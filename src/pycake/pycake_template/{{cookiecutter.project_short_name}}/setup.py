#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""

import io
import os
import sys

from setuptools import find_packages, setup
from setuptools.command.test import test as TestCommand


DESCRIPTION = '{{ cookiecutter.project_short_description }}'
{% if 'none' == cookiecutter.project_repo_url|lower %}
URL = None
{% else %}
URL = '{{ cookiecutter.project_repo_url }}'
{% endif %}
EMAIL = '{{ cookiecutter.author_email }}'
AUTHOR = "{{ cookiecutter.author_name.replace('\"', '\\\"') }}",
VERSION = None


REQUIRED = [{%- if cookiecutter.command_line_interface|lower == 'click' %}'Click>=6.0',{%- endif %} ]  # noqa

TEST_REQUIREMENTS = [
    'pytest-cov',
    'pytest-mock',
    'pytest-xdist',
    'pytest==3.9.2'
]

here = os.path.abspath(os.path.dirname(__file__))
src = os.path.join(here, 'src')


class PyTest(TestCommand):
    user_options = [('pytest-args=', 'a', "Arguments to pass into py.test")]

    def initialize_options(self):
        TestCommand.initialize_options(self)
        try:
            from multiprocessing import cpu_count
            self.pytest_args = ['-n', str(cpu_count())]
        except (ImportError, NotImplementedError):
            self.pytest_args = ['-n', '1']

    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        import pytest

        errno = pytest.main(self.pytest_args)
        sys.exit(errno)


if sys.argv[-1] == 'publish':
    os.system('python setup.py sdist')
    os.system('twine upload dist/*')
    sys.exit()

with io.open(os.path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = '\n' + f.read()


meta = {}
if VERSION is None:
    with open(os.path.join(src, '{{ cookiecutter.project_short_name }}', 'meta.py')) as f:
        exec(f.read(), meta)
else:
    meta['__version__'] = VERSION


{%- set license_classifiers = {
    'MIT license': 'License :: OSI Approved :: MIT License',
    'BSD license': 'License :: OSI Approved :: BSD License',
    'ISC license': 'License :: OSI Approved :: ISC License (ISCL)',
    'Apache Software License 2.0': 'License :: OSI Approved :: Apache Software License',
    'GNU General Public License v3': 'License :: OSI Approved :: GNU General Public License v3 (GPLv3)'
} %}


setup(
    name=meta['__name__'],
    version=meta['__version__'],
    description=DESCRIPTION,
    license='BSD',
    long_description=long_description,
    author=AUTHOR,
    author_email=EMAIL,
    url=URL,
    packages=find_packages('src'),
    package_dir={'': 'src'},
    install_requires=REQUIRED,
    include_package_data=True,
    zip_safe=False,
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
{%- if cookiecutter.open_source_license in license_classifiers %}
        '{{ license_classifiers[cookiecutter.open_source_license] }}',
{%- endif %}
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
    {%- if 'no' not in cookiecutter.command_line_interface|lower %}
    entry_points={
        'console_scripts': [
            '{{ cookiecutter.project_short_name }}={{ cookiecutter.project_short_name }}.cli:main',
        ],
    },
    {%- endif %}
    keywords=[
        '{{ cookiecutter.project_short_name }}',
    ],
    cmdclass={'test': PyTest},
    tests_require=TEST_REQUIREMENTS,
    setup_requires=['pytest-runner'],
    extras_require={
        'dev': ['check-manifest'],
        'test': ['coverage'],
    },
)
