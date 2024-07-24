#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu

import http
import logging
import urllib.parse

from bson import ObjectId
from flask import request, jsonify, make_response
from marshmallow import Schema, fields, ValidationError

from settings import (
    ZIMIT_IMAGE,
    TASK_CPU,
    TASK_MEMORY,
    TASK_DISK,
    ZIMIT_SIZE_LIMIT,
    ZIMIT_TIME_LIMIT,
    CALLBACK_BASE_URL,
    HOOK_TOKEN,
    TASK_WORKER,
)
from zimfarm import query_api
from utils import jinja_env, send_email_via_mailgun, get_context
from routes import API_PREFIX
from routes.base import BaseRoute, BaseBlueprint
from routes.errors import InvalidRequestJSON, InternalError, Unauthorized, BadRequest

logger = logging.getLogger(__name__)


class RequestSchema(Schema):
    url = fields.Url(required=True)
    email = fields.Email(required=False)
    flags = fields.Dict(required=True)


class RequestsRoute(BaseRoute):
    rule = "/"
    name = "requests"
    methods = ["POST"]

    def post(self, *args, **kwargs):
        # validate inputs
        try:
            document = RequestSchema().load(request.get_json())
            url = urllib.parse.urlparse(document.get("url", ""))
            # overwrite flags url
            document["flags"]["url"] = url.geturl()
        except ValidationError as e:
            raise InvalidRequestJSON(e.messages)

        ident = str(ObjectId())[::-1][:8]

        # build zimit config
        document["flags"]["name"] = document["flags"].get(
            "name", f"{url.hostname}_{ident}"
        )

        document["flags"]["zim-file"] = (
            document["flags"].get("zim-file", url.hostname) + f"_{ident}.zim"
        )

        document["flags"]["userAgentSuffix"] = "zimit.kiwix.org+"

        # remove flags we don't want to overwrite
        for flag in ("adminEmail", "output", "statsFilename"):
            if flag in document["flags"]:
                del document["flags"][flag]

        # make sure we cap requests to ZIMIT_LIMIT at most
        def _cap_limit(user_limit: int, zimit_limit: int) -> int:
            if user_limit <= 0:  # case where someone is trying to trick the limit
                return zimit_limit
            if user_limit < zimit_limit:
                return user_limit
            return zimit_limit  # case where someone is trying to trick as well

        try:
            size_limit = int(document["flags"].get("sizeLimit", ZIMIT_SIZE_LIMIT))
        except Exception:
            size_limit = ZIMIT_SIZE_LIMIT
        document["flags"]["sizeLimit"] = str(_cap_limit(size_limit, ZIMIT_SIZE_LIMIT))
        try:
            time_limit = int(document["flags"].get("timeLimit", ZIMIT_TIME_LIMIT))
        except Exception:
            time_limit = ZIMIT_TIME_LIMIT
        document["flags"]["timeLimit"] = _cap_limit(time_limit, ZIMIT_TIME_LIMIT)

        config = {
            "task_name": "zimit",
            "warehouse_path": "/other",
            "image": {
                "name": ZIMIT_IMAGE.split(":")[0],
                "tag": ZIMIT_IMAGE.split(":")[1],
            },
            "resources": {
                "cpu": TASK_CPU,
                "memory": TASK_MEMORY,
                "disk": TASK_DISK,
                "shm": TASK_MEMORY,
                "cap_add": ["SYS_ADMIN", "NET_ADMIN"],
            },
            "platform": None,
            "monitor": False,
            "flags": document["flags"],
        }

        # gen schedule name
        schedule_name = f"{url.hostname}_{ident}"
        # create schedule payload
        payload = {
            "name": schedule_name,
            "language": {"code": "eng", "name_en": "English", "name_native": "English"},
            "category": "other",
            "periodicity": "manually",
            "tags": [],
            "enabled": True,
            "config": config,
        }

        # add notification callback if email supplied
        if document.get("email"):
            url = f"{CALLBACK_BASE_URL}?token={HOOK_TOKEN}&target={document['email']}"
            payload.update(
                {
                    "notification": {
                        "requested": {"webhook": [url]},
                        "ended": {"webhook": [url]},
                    }
                }
            )

        # create a unique schedule for that request on the zimfarm
        success, status, resp = query_api("POST", "/schedules/", payload=payload)
        if not success:
            logger.error(f"Unable to create schedule via HTTP {status}: {resp}")
            message = f"Unable to create schedule via HTTP {status}: {resp}"
            if status == http.HTTPStatus.BAD_REQUEST:
                # if Zimfarm replied this is a bad request, then this is most probably
                # a bad request due to user input so we can track it like a bad request
                raise BadRequest(message)
            else:
                # otherwise, this is most probably an internal problem in our systems
                raise InternalError(message)

        # request a task for that newly created schedule
        success, status, resp = query_api(
            "POST",
            "/requested-tasks/",
            payload={"schedule_names": [schedule_name], "worker": TASK_WORKER},
        )
        if not success:
            logger.error(f"Unable to request {schedule_name} via HTTP {status}: {resp}")
            raise InternalError(
                f"Unable to request schedule via HTTP {status}): {resp}"
            )

        try:
            task_id = resp.get("requested").pop()
            if not task_id:
                raise InternalError("task_id is False")
        except Exception as exc:
            raise InternalError(f"Couldn't retrieve requested task id: {exc}")

        # remove newly created schedule (not needed anymore)
        success, status, resp = query_api("DELETE", f"/schedules/{schedule_name}")
        if not success:
            logger.error(
                f"Unable to remove schedule {schedule_name} via HTTP {status}: {resp}"
            )
        return make_response(jsonify({"id": str(task_id)}), http.HTTPStatus.CREATED)


class RequestRoute(BaseRoute):
    rule = "/<string:request_id>"
    name = "request"
    methods = ["GET"]

    def get(self, request_id: str):
        success, status, task = query_api("GET", f"/tasks/{request_id}")
        if status == 404:
            success, status, task = query_api("GET", f"/requested-tasks/{request_id}")

        if not success:
            return jsonify({"error": task}), status if isinstance(status, int) else 500

        # clear notification details and replace with `has_email` boolean
        if isinstance(task, dict):
            try:
                task["has_email"] = bool(task["notification"]["ended"]["webhook"])
            except Exception:
                task["has_email"] = False
            task["notification"] = None

        return jsonify(task), status


class RequestsHookRoute(BaseRoute):
    rule = "/hook"
    name = "request-hook"
    methods = ["POST"]

    def post(self, *args, **kwargs):
        # we require a `token` arg equal to a setting string so we can ensure
        # hook requests are from know senders.
        # otherwises exposes us to spam abuse
        if request.args.get("token") != HOOK_TOKEN:
            raise Unauthorized("Identify via proper token to use hook")

        # without a `target` arg, we have nowhere to send the notification to
        target = request.args.get("target")
        if not target:
            return jsonify({"status": "failed"})

        if not isinstance(request.json, dict):
            raise BadRequest("malformed webhook request")

        context = get_context(request.json)
        status = context["task"].get("status")
        # discard hooks registered for events we don't plan on sending email for
        if status not in ("requested", "succeeded", "failed", "canceled"):
            return jsonify({"status": "success"})

        subject = jinja_env.get_template("email_subject.txt").render(**context)
        body = jinja_env.get_template("email_body.html").render(**context)
        send_email_via_mailgun(target, subject, body)

        return jsonify({"status": "success"})


class Blueprint(BaseBlueprint):
    def __init__(self):
        super().__init__("requests", __name__, url_prefix=f"{API_PREFIX}/requests")

        self.register_route(RequestsRoute())
        self.register_route(RequestRoute())
        self.register_route(RequestsHookRoute())
