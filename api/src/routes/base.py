#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu

import logging
from http import HTTPStatus

from flask import request, Response, Blueprint

logger = logging.getLogger(__name__)


class BaseRoute:
    rule = ""
    name = ""
    methods = []

    def __call__(self, *args, **kwargs):
        handlers = {
            "GET": self.get,
            "POST": self.post,
            "PUT": self.put,
            "PATCH": self.patch,
            "DELETE": self.delete,
        }
        handler = handlers[request.method]
        return handler(*args, **kwargs)

    def get(self, *args, **kwargs):
        return Response(status=HTTPStatus.METHOD_NOT_ALLOWED)

    def post(self, *args, **kwargs):
        return Response(status=HTTPStatus.METHOD_NOT_ALLOWED)

    def put(self, *args, **kwargs):
        return Response(status=HTTPStatus.METHOD_NOT_ALLOWED)

    def patch(self, *args, **kwargs):
        return Response(status=HTTPStatus.METHOD_NOT_ALLOWED)

    def delete(self, *args, **kwargs):
        return Response(status=HTTPStatus.METHOD_NOT_ALLOWED)


class BaseBlueprint(Blueprint):
    def register_route(self, route: BaseRoute):
        self.add_url_rule(route.rule, route.name, route, methods=route.methods)
