#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu

import os
import logging

logger = logging.getLogger(__name__)


ZIMFARM_API_URL = os.getenv("ZIMFARM_WEBAPI", "https://api.farm.openzim.org/v1")
ZIMFARM_USERNAME = os.getenv("_ZIMFARM_USERNAME", "-")
ZIMFARM_PASSWORD = os.getenv("_ZIMFARM_PASSWORD", "-")
