#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu

from uuid import UUID
from datetime import datetime

from bson.objectid import ObjectId
from flask.json import JSONEncoder


class ZimitEncoder(JSONEncoder):
    def default(self, o):
        if isinstance(o, datetime):
            return o.isoformat() + "Z"
        if isinstance(o, UUID):
            return str(o)
        if isinstance(o, ObjectId):
            return str(o)
        super().default(o)
