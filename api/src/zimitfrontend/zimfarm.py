import datetime
import json
import logging
from collections.abc import Callable
from http import HTTPStatus
from typing import Any, ParamSpec, TypeVar

import requests

from zimitfrontend.constants import ApiConfiguration

GET = "GET"
POST = "POST"
PATCH = "PATCH"
DELETE = "DELETE"

logger = logging.getLogger(__name__)


class TokenData:
    ACCESS_TOKEN: str | None = None
    ACCESS_TOKEN_EXPIRY: datetime.datetime | None = None
    REFRESH_TOKEN: str | None = None
    REFRESH_TOKEN_EXPIRY: datetime.datetime | None = None


class ZimfarmAPIError(Exception):
    pass


def get_url(path: str) -> str:
    return "/".join(
        [ApiConfiguration.zimfarm_api_url, path[1:] if path[0] == "/" else path]
    )


def get_token_headers(token: str) -> dict[str, str]:
    return {
        "Authorization": f"Token {token}",
        "Content-type": "application/json",
    }


def get_token(username: str, password: str) -> tuple[str, str]:
    req = requests.post(
        url=get_url("/auth/authorize"),
        headers={
            "username": username,
            "password": password,
            "Content-type": "application/json",
        },
        timeout=ApiConfiguration.zimfarm_requests_timeout,
    )
    req.raise_for_status()
    return req.json().get("access_token"), req.json().get("refresh_token")


def authenticate(*, force: bool = False) -> None:
    if (
        not force
        and TokenData.ACCESS_TOKEN is not None
        and TokenData.ACCESS_TOKEN_EXPIRY is not None
        and TokenData.ACCESS_TOKEN_EXPIRY
        > datetime.datetime.now(tz=datetime.UTC) + datetime.timedelta(minutes=2)
    ):
        return

    logger.debug(f"authenticate() with force={force}")

    try:
        access_token, refresh_token = get_token(
            username=ApiConfiguration.zimfarm_username,
            password=ApiConfiguration.zimfarm_password,
        )
    except Exception:
        TokenData.ACCESS_TOKEN = TokenData.REFRESH_TOKEN = (
            TokenData.ACCESS_TOKEN_EXPIRY
        ) = None
    else:
        TokenData.ACCESS_TOKEN, TokenData.REFRESH_TOKEN = access_token, refresh_token
        TokenData.ACCESS_TOKEN_EXPIRY = datetime.datetime.now(
            tz=datetime.UTC
        ) + datetime.timedelta(minutes=59)
        TokenData.REFRESH_TOKEN_EXPIRY = datetime.datetime.now(
            tz=datetime.UTC
        ) + datetime.timedelta(days=29)


# Generic type variable for the return type of the wrapped function
R = TypeVar("R")

# ParamSpec for capturing the signature of the wrapped function
P = ParamSpec("P")


def auth_required(func: Callable[P, R]) -> Callable[P, R]:
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
        authenticate()
        return func(*args, **kwargs)

    return wrapper


@auth_required
def query_api(
    method: str, path: str, payload: Any | None = None, params: Any | None = None
) -> tuple[bool, HTTPStatus, Any]:
    if not TokenData.ACCESS_TOKEN:
        return (
            False,
            HTTPStatus.INTERNAL_SERVER_ERROR,
            "Authentication on Zimfarm failed",
        )
    try:
        req = requests.request(
            method.lower(),
            url=get_url(path),
            headers=get_token_headers(TokenData.ACCESS_TOKEN),
            json=payload,
            params=params,
            timeout=ApiConfiguration.zimfarm_requests_timeout,
        )
    except Exception as exc:
        logger.exception(exc)
        return (False, HTTPStatus.REQUEST_TIMEOUT, f"ConnectionError -- {exc}")

    try:
        resp: Any = req.json() if req.text else {}
    except json.JSONDecodeError:
        return (
            False,
            HTTPStatus(req.status_code),
            f"ResponseError (not JSON): -- {req.text}",
        )
    except Exception as exc:
        return (
            False,
            HTTPStatus(req.status_code),
            f"ResponseError -- {exc} -- {req.text}",
        )

    if HTTPStatus(req.status_code).is_success:
        return True, HTTPStatus(req.status_code), resp

    # Unauthorised error: attempt to re-auth as scheduler might have restarted?
    if req.status_code == HTTPStatus.UNAUTHORIZED:
        authenticate(force=True)

    reason = resp["error"] if "error" in resp else str(resp)
    if "error_description" in resp:
        reason = f"{reason}: {resp['error_description']}"
    return (False, HTTPStatus(req.status_code), reason)


@auth_required
def test_connection():
    return query_api(GET, "/auth/test")
