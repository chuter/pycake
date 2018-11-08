#!/usr/bin/env python
# -*- encoding: utf-8 -*-

import os

CUR_DIR = os.path.dirname(os.path.abspath(__file__))
TEMPLATE_PATH = os.path.join(CUR_DIR, 'pycake_template')


def prepare():
    """
    Prepare all the stuff for start a new Python project.

    This function use cookiecutter(https://github.com/audreyr/cookiecutter)
    The template dir is ./project_template

    """
    from cookiecutter.main import cookiecutter

    return cookiecutter(TEMPLATE_PATH)
