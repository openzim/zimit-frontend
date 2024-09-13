from collections.abc import Sequence
from pathlib import Path

import humanfriendly
import requests
from jinja2 import Environment, FileSystemLoader, select_autoescape

from zimitfrontend import i18n
from zimitfrontend.constants import ApiConfiguration
from zimitfrontend.logging import get_logger

logger = get_logger(__name__)

i18n.setup_i18n()

jinja_env = Environment(
    loader=FileSystemLoader(Path(__file__).parent / "templates"),
    autoescape=select_autoescape(["html", "txt"]),
)
jinja_env.filters["short_id"] = lambda value: str(value)[:5]
jinja_env.filters["format_size"] = lambda value: humanfriendly.format_size(
    value, binary=True  # pyright: ignore[reportArgumentType]
)
jinja_env.filters["format_timespan"] = lambda value: humanfriendly.format_timespan(
    value  # pyright: ignore[reportArgumentType]
)
jinja_env.globals["translate"] = i18n.t  # pyright: ignore


def send_email_via_mailgun(
    to: Sequence[str],
    subject: str,
    contents: str,
    cc: Sequence[str] | None = None,
    bcc: Sequence[str] | None = None,
) -> str | None:
    """Send email via mailgun and return task id"""
    if not ApiConfiguration.mailgun_api_url or not ApiConfiguration.mailgun_api_key:
        logger.warning("Email not sent, Mailgun is not properly configured")
        return

    resp = requests.post(
        url=f"{ApiConfiguration.mailgun_api_url}/messages",
        auth=("api", ApiConfiguration.mailgun_api_key),
        data={
            "from": ApiConfiguration.mailgun_from,
            "subject": subject,
            "html": contents,
            "to": to,  # can be a list, will be handle properly by requests
            "cc": cc,  # can be a list
            "bcc": bcc,  # can be a list
        },
        timeout=ApiConfiguration.mailgun_requests_timeout,
    )
    resp.raise_for_status()
    return resp.json().get("id") or resp.text
