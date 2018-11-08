#!/usr/bin/env python
# -*- coding: utf-8 -*-

import io
import os
import sys

from setuptools import find_packages, setup
from setuptools.command.test import test as TestCommand


DESCRIPTION = 'Python Project Management Tool to Simplify teammate Py Life'
URL = 'https://github.com/chuter/pycake'
EMAIL = 'topgun.chuter@gmail.com'
AUTHOR = 'chuter'
VERSION = None

REQUIRED = [
    'click',
    'crayons',
    'cookiecutter'
]

TEST_REQUIREMENTS = [
    'click',
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
    with open(os.path.join(src, 'pycake', 'meta.py')) as f:
        exec(f.read(), meta)
else:
    meta['__version__'] = VERSION


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
    python_requires=">=2.7,!=3.0.*,!=3.1.*,!=3.2.*,!=3.3.*",
    package_dir={'': 'src'},
    install_requires=REQUIRED,
    include_package_data=True,
    zip_safe=False,
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Natural Language :: Chinese (Simplified)',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Topic :: Software Development',
    ],
    keywords=[
        'python', 'develop', 'starter', 'manage tool', 'lifecycle'
    ],
    entry_points={
        'console_scripts': [
            'pycake=pycake:cli',
            'py.cake=pycake:cli',
        ],
    },
    cmdclass={'test': PyTest},
    tests_require=TEST_REQUIREMENTS,
    setup_requires=['pytest-runner'],
    extras_require={
        'dev': ['check-manifest'],
        'test': ['coverage'],
    },
)
