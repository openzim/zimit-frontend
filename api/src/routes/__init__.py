#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu

import os
import logging

logger = logging.getLogger(__name__)

MAIN_PREFIX = os.getenv("MAIN_PREFIX", "")
API_PREFIX = "/".join((MAIN_PREFIX, "v1"))
