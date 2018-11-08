#!/usr/bin/env python
# -*- encoding: utf-8 -*-

# flake8: noqa

import re
import sys


MODULE_REGEX = r'^[_a-zA-Z][_a-zA-Z0-9]+$'

module_name = '{{ cookiecutter.project_short_name}}'

if not re.match(MODULE_REGEX, module_name):
    print('ERROR: The project short name (%s) is not a valid Python module name. Please do not use a - and use _ instead' % module_name)

    # Exit to cancel project
    sys.exit(1)
