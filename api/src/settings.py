#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu

import os
import uuid
import logging

import humanfriendly

logger = logging.getLogger(__name__)

DEFAULT_CPU = 3
DEFAULT_MEMORY = "1GiB"
DEFAULT_DISK = "1GiB"
ZIMFARM_API_URL = os.getenv("ZIMFARM_WEBAPI", "https://api.farm.youzim.it/v1")
ZIMFARM_USERNAME = os.getenv("_ZIMFARM_USERNAME", "-")
ZIMFARM_PASSWORD = os.getenv("_ZIMFARM_PASSWORD", "-")
ZIMIT_IMAGE = os.getenv("ZIMIT_IMAGE", "openzim/zimit:dev")
try:
    TASK_CPU = int(os.getenv("TASK_CPU", DEFAULT_CPU))
except Exception as exc:
    logger.error(
        f"Unable to apply custom TASK_CPU: {os.getenv('TASK_CPU')}. "
        f"Using {DEFAULT_CPU}. Error: {exc}"
    )
    TASK_CPU = DEFAULT_CPU
try:
    TASK_MEMORY = humanfriendly.parse_size(os.getenv("TASK_MEMORY", DEFAULT_MEMORY))
except Exception as exc:
    logger.error(
        f"Unable to apply custom TASK_MEMORY: {os.getenv('TASK_MEMORY')}. "
        f"Using {DEFAULT_MEMORY}. Error: {exc}"
    )
    TASK_MEMORY = humanfriendly.parse_size(DEFAULT_MEMORY)
try:
    TASK_DISK = humanfriendly.parse_size(os.getenv("TASK_DISK", DEFAULT_DISK))
except Exception as exc:
    logger.error(
        f"Unable to apply custom TASK_DISK: {os.getenv('TASK_DISK')}. "
        f"Using {DEFAULT_DISK}. Error: {exc}"
    )
    TASK_DISK = humanfriendly.parse_size(DEFAULT_DISK)

# mailgun
MAILGUN_FROM = os.getenv("MAILGUN_FROM", "Youzim.it <info@youzim.it>")
MAILGUN_API_KEY = os.getenv("MAILGUN_API_KEY", "")
MAILGUN_API_URL = os.getenv(
    "MAILGUN_API_URL", "https://api.mailgun.net/v3/mg.youzim.it"
)
# notifications callback
PUBLIC_URL = os.getenv("PUBLIC_URL", "https://youzim.it")
PUBLIC_API_URL = os.getenv("PUBLIC_API_URL", "https://youzim.it/api/v1")
ZIM_DOWNLOAD_URL = os.getenv(
    "ZIM_DOWNLOAD_URL", "https://s3.us-west-1.wasabisys.com/org-kiwix-zimit/zim"
)
CALLBACK_BASE_URL = os.getenv("CALLBACK_BASE_URL", f"{PUBLIC_API_URL}/requests/hook")
HOOK_TOKEN = os.getenv("HOOK_TOKEN", uuid.uuid4().hex)
