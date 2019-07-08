# -*- encoding: utf-8 -*-
from __future__ import absolute_import

import logging


logger = logging.getLogger(__name__)


def echo(content):
    logger.info(content)
    return content
