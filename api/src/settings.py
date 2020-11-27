#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu

import os
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
