#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu

import json
import logging
import datetime

import requests

from settings import ZIMFARM_API_URL, ZIMFARM_USERNAME, ZIMFARM_PASSWORD

GET = "GET"
POST = "POST"
PATCH = "PATCH"
DELETE = "DELETE"
ACCESS_TOKEN = None
ACCESS_TOKEN_EXPIRY = None
REFRESH_TOKEN = None
REFRESH_TOKEN_EXPIRY = None

logger = logging.getLogger(__name__)


class ZimfarmAPIError(Exception):
    pass


def get_url(path):
    return "/".join([ZIMFARM_API_URL, path[1:] if path[0] == "/" else path])


def get_token_headers(token):
    return {
        "Authorization": "Token {}".format(token),
        "Content-type": "application/json",
    }


def get_token(username, password):
    req = requests.post(
        url=get_url("/auth/authorize"),
        headers={
            "username": username,
            "password": password,
            "Content-type": "application/json",
        },
    )
    req.raise_for_status()
    return req.json().get("access_token"), req.json().get("refresh_token")


def authenticate(force=False):
    global ACCESS_TOKEN, REFRESH_TOKEN, ACCESS_TOKEN_EXPIRY, REFRESH_TOKEN_EXPIRY

    if (
        not force
        and ACCESS_TOKEN is not None
        and ACCESS_TOKEN_EXPIRY
        > datetime.datetime.now() + datetime.timedelta(minutes=2)
    ):
        return

    logger.debug("authenticate() with force={}".format(force))

    try:
        access_token, refresh_token = get_token(
            username=ZIMFARM_USERNAME, password=ZIMFARM_PASSWORD
        )
    except Exception:
        ACCESS_TOKEN = REFRESH_TOKEN = ACCESS_TOKEN_EXPIRY = None
    else:
        ACCESS_TOKEN, REFRESH_TOKEN = access_token, refresh_token
        ACCESS_TOKEN_EXPIRY = datetime.datetime.now() + datetime.timedelta(minutes=59)
        REFRESH_TOKEN_EXPIRY = datetime.datetime.now() + datetime.timedelta(days=29)


def auth_required(func):
    def wrapper(*args, **kwargs):
        authenticate()
        return func(*args, **kwargs)

    return wrapper


@auth_required
def query_api(method, path, payload=None, params=None):
    try:
        req = getattr(requests, method.lower(), "get")(
            url=get_url(path),
            headers=get_token_headers(ACCESS_TOKEN),
            json=payload,
            params=params,
        )
    except Exception as exc:
        logger.exception(exc)
        return (False, "ConnectionError", "ConnectionError -- {}".format(exc))

    try:
        resp = req.json() if req.text else {}
    except json.JSONDecodeError:
        return (
            False,
            req.status_code,
            "ResponseError (not JSON): -- {}".format(req.text),
        )
    except Exception as exc:
        return (
            False,
            req.status_code,
            "ResponseError -- {} -- {}".format(str(exc), req.text),
        )

    if req.status_code >= 200 and req.status_code < 300:
        return True, req.status_code, resp

    # Unauthorised error: attempt to re-auth as scheduler might have restarted?
    if req.status_code == 401:
        authenticate(True)

    return (False, req.status_code, resp["error"] if "error" in resp else str(resp))


@auth_required
def test_connection():
    return query_api(GET, "/auth/test")
