# -*- encoding: utf-8 -*-

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
app = connexion.FlaskApp(
    __name__,
    port=EXPOSE,
    specification_dir='.app/',
    server='tornado'
)

{% for yaml in cookiecutter.app.openapi_ymls %}
app.add_api('{{ yaml }}.yaml')
{% endfor %}


# ms
# app.add_api('monitor.yaml')
# app.add_api('manage.yaml')

app.run()
