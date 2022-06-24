#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu
import logging
from typing import Optional, Sequence

import requests
import humanfriendly
from uuid import UUID
from datetime import datetime
from bson.objectid import ObjectId
from flask.json import JSONEncoder
from jinja2 import Environment, FileSystemLoader, select_autoescape
from werkzeug.datastructures import MultiDict

from settings import (
    MAILGUN_API_KEY,
    MAILGUN_API_URL,
    MAILGUN_FROM,
    PUBLIC_URL,
    ZIM_DOWNLOAD_URL,
    ZIMIT_LIMIT,
)

logger = logging.getLogger(__name__)
jinja_env = Environment(
    loader=FileSystemLoader("templates"),
    autoescape=select_autoescape(["html", "txt"]),
)
jinja_env.filters["short_id"] = lambda value: str(value)[:5]
jinja_env.filters["format_size"] = lambda value: humanfriendly.format_size(
    value, binary=True
)


class ZimitEncoder(JSONEncoder):
    def default(self, o):
        if isinstance(o, datetime):
            return o.isoformat() + "Z"
        if isinstance(o, UUID):
            return str(o)
        if isinstance(o, ObjectId):
            return str(o)
        super().default(o)


def send_email_via_mailgun(
    to: Sequence[str],
    subject: str,
    contents: str,
    cc: Optional[Sequence] = None,
    bcc: Optional[Sequence] = None,
    headers: Optional[dict] = None,
    attachments: Optional[Sequence] = None,
):
    if not MAILGUN_API_URL or not MAILGUN_API_KEY:
        return

    values = [
        ("from", MAILGUN_FROM),
        ("subject", subject),
        ("html", contents),
    ]
    values += [("to", to if isinstance(to, (list, tuple)) else [to])]
    values += [("cc", cc if isinstance(cc, (list, tuple)) else [cc])]
    values += [("bcc", bcc if isinstance(bcc, (list, tuple)) else [bcc])]
    data = MultiDict(values)

    try:
        resp = requests.post(
            url=f"{MAILGUN_API_URL}/messages",
            auth=("api", MAILGUN_API_KEY),
            data=data,
            files=[
                ("attachment", (fpath.name, open(fpath, "rb").read()))
                for fpath in attachments
            ]
            if attachments
            else [],
        )
        resp.raise_for_status()
    except Exception as exc:
        logger.error(f"Failed to send mailgun notif: {exc}")
        logger.exception(exc)
    return resp.json().get("id") or resp.text


def get_context(task):
    """Jinja context dict for email notifications"""
    return {
        "base_url": PUBLIC_URL,
        "download_url": ZIM_DOWNLOAD_URL,
        "limit": ZIMIT_LIMIT,
        "task": task,
    }
