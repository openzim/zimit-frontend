import os
import pathlib
import uuid

import humanfriendly

from zimitfrontend.logging import get_logger

src_dir = pathlib.Path(__file__).parent.resolve()

logger = get_logger(
    "zimitfrontend",
    level=os.getenv(
        "LOG_LEVEL",
        "INFO",
    ),
)


def _get_int_setting(environment_variable_name: str, default_value: int) -> int:
    """Get environment variable as integer or fallback to default value"""
    try:
        return int(os.getenv(environment_variable_name) or default_value)
    except Exception as exc:
        logger.error(
            f"Unable to parse {environment_variable_name}: "
            f"{os.getenv(environment_variable_name)}."
            f"Using {default_value}. Error: {exc}"
        )
        return default_value


def _get_size_setting(environment_variable_name: str, default_value: str) -> int:
    """Get environment variable as size (parsed with unit) or fallback to default"""
    try:
        return humanfriendly.parse_size(
            os.getenv(environment_variable_name) or default_value
        )
    except Exception as exc:
        logger.error(
            f"Unable to apply custom {environment_variable_name}: "
            f"{os.getenv(environment_variable_name)}. "
            f"Using {default_value}. Error: {exc}"
        )
        return humanfriendly.parse_size(default_value)


def _get_time_setting(environment_variable_name: str, default_value: str) -> float:
    """Get environment variable as time (parsed with unit) or fallback to default

    Returned value is in seconds, not matter the unit passed in environement variable
    """
    try:
        return humanfriendly.parse_timespan(
            os.getenv(environment_variable_name) or default_value
        )
    except Exception as exc:
        logger.error(
            f"Unable to apply custom {environment_variable_name}: "
            f"{os.getenv(environment_variable_name)}. "
            f"Using {default_value}. Error: {exc}"
        )
        return humanfriendly.parse_timespan(default_value)


class ApiConfiguration:
    """Shared backend configuration"""

    allowed_origins: list[str] = os.getenv(
        "ALLOWED_ORIGINS",
        "http://localhost|http://localhost:8000|http://localhost:8080",  # dev fallback
    ).split("|")

    zimfarm_api_url = os.getenv(
        "INTERNAL_ZIMFARM_WEBAPI", "https://api.farm.zimit.kiwix.org/v1"
    )
    zimfarm_requests_timeout = _get_time_setting("ZIMFARM_REQUESTS_TIMEOUT", "10s")
    mailgun_requests_timeout = _get_time_setting("MAILGUN_REQUESTS_TIMEOUT", "10s")
    zimfarm_username = os.getenv("_ZIMFARM_USERNAME", "-")
    zimfarm_password = os.getenv("_ZIMFARM_PASSWORD", "-")
    zimit_image = os.getenv("ZIMIT_IMAGE", "openzim/zimit:1.2.0")

    zimit_size_limit = _get_int_setting("ZIMIT_SIZE_LIMIT", 2**30 * 4)
    zimit_time_limit = _get_int_setting("ZIMIT_TIME_LIMIT", 3600 * 2)

    task_cpu = _get_int_setting("TASK_CPU", 3)
    task_memory = _get_size_setting("TASK_MEMORY", "1GiB")
    task_disk = _get_size_setting("TASK_DISK", "1GiB")

    task_worker = os.getenv("TASK_WORKER")

    # mailgun
    mailgun_from = os.getenv("MAILGUN_FROM", "Zimit <info@zimit.kiwix.org>")
    mailgun_api_key = os.getenv("MAILGUN_API_KEY")
    mailgun_api_url = os.getenv(
        "MAILGUN_API_URL", "https://api.mailgun.net/v3/mg.zimit.kiwix.org"
    )

    public_url = os.getenv("PUBLIC_URL", "https://zimit.kiwix.org")
    public_api_url = os.getenv("PUBLIC_API_URL", "https://zimit.kiwix.org/api/v1")
    zim_download_url = os.getenv(
        "ZIM_DOWNLOAD_URL", "https://s3.us-west-1.wasabisys.com/org-kiwix-zimit/zim"
    )
    contact_us_url = os.getenv("CONTACT_US_URL", "https://www.kiwix.org/en/contact/")

    # notifications callback
    callback_base_url = os.getenv(
        "CALLBACK_BASE_URL", "https://zimit.kiwix.org/api/v1/hook"
    )
    hook_token = os.getenv("HOOK_TOKEN", uuid.uuid4().hex)

    locales_location = pathlib.Path(os.getenv("LOCALES_LOCATION", "../locales"))

    # list of rtl language codes
    rtl_language_codes = ("fa", "he")
