# -*- encoding: utf-8 -*-
from __future__ import absolute_import

import logging


logger = logging.getLogger(__name__)

{% if cookiecutter.app.openapi_model == 'True' %}
def predict(input: dict = {'features':{}}):
    return 0.9
{% else %}
def echo(content):
    logger.info(content)
    return content
{% endif %}