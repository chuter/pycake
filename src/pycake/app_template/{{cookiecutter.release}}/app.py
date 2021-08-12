# -*- encoding: utf-8 -*-
from __future__ import absolute_import

import os
import sys
import yaml

import logging.config
import connexion

#
# ==================================================
#                 build env
# ==================================================
#
def setup_logging( # noqa
    default_path='config/logging.yaml',
    default_level=logging.INFO,
    env_key='LOG_CFG'
):
    path = default_path
    value = os.getenv(env_key, None)
    if value:
        path = value
    if os.path.exists(path):
        with open(path, 'rt') as f:
            config = yaml.safe_load(f.read())
        logging.config.dictConfig(config)
    else:
        logging.basicConfig(level=default_level)


def build_env():
    sys.path.insert(0, 'lib')

    log_settings_path = os.path.join('config', 'logging.yaml')
    setup_logging(default_path=log_settings_path)


APP_NAME = '{{cookiecutter.app.app_name}}'
EXPOSE = 9502

build_env()
logger = logging.getLogger(APP_NAME)


#
# ==================================================
#                 start app
# ==================================================
#
app = connexion.AioHttpApp(
    __name__,
    port=EXPOSE,
    specification_dir='.app/'
)

{% if cookiecutter.app.model_sample == 'True' %}
from middleware import build_model_sample_middleware # noqa
{% if 'model_name' in cookiecutter.app %}
app.app.middlewares.append(build_model_sample_middleware(
    '{{cookiecutter.app.model_sample_api}}',
    sample_ratio=os.environ.get('model_sample_ratio', None) or {{cookiecutter.app.model_sample_ratio|int}},
    model_name='{{cookiecutter.app.model_name}}',
    model_version='{{cookiecutter.app.model_version|replace('_', '.')}}'
))
{% else %}
app.app.middlewares.append(build_model_sample_middleware(
    '{{cookiecutter.app.model_sample_api}}',
    sample_ratio=os.environ.get('model_sample_ratio', None) or {{cookiecutter.app.model_sample_ratio|int}}
))
{%- endif -%}
{%- endif -%}

{% for yaml in cookiecutter.app.openapi_ymls %}
app.add_api('{{ yaml }}.yaml')
{% endfor %}


# ms
app.add_api('monitor.yaml')
# app.add_api('manage.yaml')

app.run()
