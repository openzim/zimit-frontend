#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu

import logging
from typing import Optional
from http import HTTPStatus

from flask import Flask, Response, jsonify, make_response

import marshmallow.exceptions

logger = logging.getLogger(__name__)


class HTTPBase(Exception):
    def __init__(
        self, status_code: HTTPStatus, error: str, description: Optional[str] = None
    ):
        self.status_code = status_code
        self.error = error
        self.description = description

    @staticmethod
    def handler(error):
        response = {"error": error.error}
        if error.description is not None:
            response["error_description"] = error.description

        response = jsonify(response)
        response.status_code = error.status_code.value
        return response


class InvalidRequestJSON(HTTPBase):
    def __init__(self, description: Optional[str] = None):
        super().__init__(HTTPStatus.BAD_REQUEST, "Invalid Request JSON", description)


class ResourceNotFound(HTTPBase):
    def __init__(self, error: str):
        if error is None:
            error = "Resource Not Found"
        super().__init__(HTTPStatus.NOT_FOUND, error)


class ScheduleNotFound(ResourceNotFound):
    def __init__(self):
        super().__init__("Schedule Not Found")


class TaskNotFound(ResourceNotFound):
    def __init__(self):
        super().__init__("Task Not Found")


def register_handlers(app: Flask):
    app.errorhandler(BadRequest)(BadRequest.handler)
    app.errorhandler(Unauthorized)(Unauthorized.handler)
    app.errorhandler(NotFound)(NotFound.handler)
    app.errorhandler(InternalError)(InternalError.handler)

    app.errorhandler(HTTPBase)(HTTPBase.handler)

    @app.errorhandler(marshmallow.exceptions.ValidationError)
    def handler_validationerror(e):
        return make_response(jsonify({"message": e.messages}), HTTPStatus.BAD_REQUEST)


# 400
class BadRequest(Exception):
    def __init__(self, message: str = None):
        self.message = message

    @staticmethod
    def handler(e):
        if isinstance(e, BadRequest) and e.message is not None:
            return make_response(jsonify({"error": e.message}), HTTPStatus.BAD_REQUEST)
        return Response(status=HTTPStatus.BAD_REQUEST)


# 401
class Unauthorized(Exception):
    def __init__(self, message: str = None):
        self.message = message

    @staticmethod
    def handler(e):
        if isinstance(e, Unauthorized) and e.message is not None:
            return make_response(jsonify({"error": e.message}), HTTPStatus.UNAUTHORIZED)
        return Response(status=HTTPStatus.UNAUTHORIZED)


# 404
class NotFound(Exception):
    def __init__(self, message: str = None):
        self.message = message

    @staticmethod
    def handler(e):
        if isinstance(e, NotFound) and e.message is not None:
            return make_response(jsonify({"error": e.message}), HTTPStatus.NOT_FOUND)
        return Response(status=HTTPStatus.NOT_FOUND)


# 500
class InternalError(Exception):
    @staticmethod
    def handler(e):
        return Response(status=HTTPStatus.INTERNAL_SERVER_ERROR)
