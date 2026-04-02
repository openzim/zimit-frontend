import datetime
import json
import logging
from collections.abc import Callable
from http import HTTPStatus
from typing import Any, ParamSpec, TypeVar, cast

import requests
from requests.auth import HTTPBasicAuth

from zimitfrontend.constants import ApiConfiguration

GET = "GET"
POST = "POST"
PATCH = "PATCH"
DELETE = "DELETE"

logger = logging.getLogger(__name__)


class ZimfarmAPIError(Exception):
    pass


def getnow():
    """naive UTC now"""
    return datetime.datetime.now(datetime.UTC).replace(tzinfo=None)


class ZimfarmClientTokenProvider:
    """Client to generate access tokens to authenticate with Zimfarm API"""

    def __init__(self):
        self._access_token: str | None = None
        self._refresh_token: str | None = None
        self._expires_at: datetime.datetime = datetime.datetime.fromtimestamp(
            0, datetime.UTC
        ).replace(tzinfo=None)

    def _generate_oauth_access_token(self) -> None:
        """Generate oauth access token and update expires_at."""
        response = requests.post(
            f"{ApiConfiguration.zimfarm_oauth_issuer}/oauth2/token",
            data={
                "grant_type": "client_credentials",
                "audience": ApiConfiguration.zimfarm_oauth_audience_id,
            },
            auth=HTTPBasicAuth(
                ApiConfiguration.zimfarm_oauth_client_id,
                ApiConfiguration.zimfarm_oauth_client_secret,
            ),
            timeout=ApiConfiguration.zimfarm_requests_timeout,
        )
        response.raise_for_status()
        payload = response.json()
        self._access_token = cast(str, payload["access_token"])
        self._expires_at = getnow() + datetime.timedelta(seconds=payload["expires_in"])

    def _generate_local_access_token(self) -> None:
        if self._refresh_token:
            response = requests.post(
                f"{ApiConfiguration.zimfarm_api_url}/auth/refresh",
                json={
                    "refresh_token": self._refresh_token,
                },
                timeout=ApiConfiguration.zimfarm_requests_timeout,
            )
        else:
            response = requests.post(
                f"{ApiConfiguration.zimfarm_api_url}/auth/authorize",
                json={
                    "username": ApiConfiguration.zimfarm_username,
                    "password": ApiConfiguration.zimfarm_password,
                },
                timeout=ApiConfiguration.zimfarm_requests_timeout,
            )

        response.raise_for_status()
        payload = response.json()
        self._access_token = cast(str, payload["access_token"])
        self._refresh_token = cast(str, payload["refresh_token"])
        self._expires_at = datetime.datetime.fromisoformat(
            payload["expires_time"]
        ).replace(tzinfo=None)

    def get_access_token(self, *, force: bool = False) -> str:
        """Retrieve or generate access token depending on if token has expired."""
        now = getnow()
        if (
            self._access_token is None
            or force
            or now >= (self._expires_at - ApiConfiguration.zimfarm_token_renewal_window)
        ):
            if ApiConfiguration.auth_mode == "oauth":
                self._generate_oauth_access_token()
            elif ApiConfiguration.auth_mode == "local":
                self._generate_local_access_token()
            else:
                raise ValueError(
                    f"Unknown cms authentication mode: {ApiConfiguration.auth_mode}. "
                    "Allowed values are: 'local', 'oauth'"
                )
        if self._access_token is None:
            raise ValueError("Failed to generate access token.")
        return self._access_token

    @property
    def access_token(self):
        return self._access_token


zimfarm_client_token_provider = ZimfarmClientTokenProvider()


def get_url(path: str) -> str:
    return "/".join(
        [ApiConfiguration.zimfarm_api_url, path[1:] if path[0] == "/" else path]
    )


def get_token_headers(token: str) -> dict[str, str]:
    return {
        "Authorization": f"Bearer {token}",
        "Content-type": "application/json",
    }


def authenticate(*, force: bool = False) -> None:
    logger.debug(
        f"authenticate() with force={force}, auth_mode={ApiConfiguration.auth_mode}"
    )
    zimfarm_client_token_provider.get_access_token(force=force)


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
    if not zimfarm_client_token_provider.access_token:
        return (
            False,
            HTTPStatus.INTERNAL_SERVER_ERROR,
            "Authentication on Zimfarm failed",
        )
    try:
        req = requests.request(
            method.lower(),
            url=get_url(path),
            headers=get_token_headers(zimfarm_client_token_provider.get_access_token()),
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
