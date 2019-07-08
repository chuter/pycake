#!/usr/bin/env python
# -*- encoding: utf-8 -*-

import os
import crayons

from cookiecutter.main import cookiecutter

from .app import build_app_config, release_app


CUR_DIR = os.path.dirname(os.path.abspath(__file__))
TEMPLATE_PATH = os.path.join(CUR_DIR, 'pycake_template')
APP_TEMPLATE_PATH = os.path.join(CUR_DIR, 'app_template')


def prepare():
    """
    Prepare all the stuff for start a new Python project.

    This function use cookiecutter(https://github.com/audreyr/cookiecutter)
    The template dir is ./project_template

    """
    return cookiecutter(TEMPLATE_PATH)


def release(with_docker_file=False, **kwargs):
    """
    Release the project

    Args:
      with_docker_file: Whether to generate Dockerfile

    Returns:
      the release result messages

    """
    app_settings = build_app_config()

    release_result = release_app(
        app_settings,
        with_docker_file=with_docker_file,
        tmpl_dir=APP_TEMPLATE_PATH,
        **kwargs
    )

    return """
Release {}

{}
""".format(crayons.green("Successful!", bold=True), release_result)
