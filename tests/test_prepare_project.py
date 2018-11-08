#!/usr/bin/env python
# -*- encoding: utf-8 -*-


import subprocess
import io
import os
import pytest
from contextlib import contextmanager

from click.testing import CliRunner

import pycake


@pytest.fixture(scope="module")
def runner():
    return CliRunner()


@pytest.fixture(scope="session", autouse=True)
def default_project_slug():
    return 'project_prepared_by_pycake'


@pytest.fixture(scope="session", autouse=True)
def default_context():
    return {
        "author_name": "chuter",
        "author_email": "topgun.chuter@gmail.com",
        "project_name": "Project Prepared By PyCake",
        "project_short_name": "project_prepared_by_pycake",
        "project_short_description": "What problem your project to resolve.",
        "version": "0.1.0",
        "project_repo_url": "https://github.com/chuter/project_prepared_by_pycake",  # noqa
        "create_author_file": "y",
        "open_source_license": "MIT license",
        "command_line_interface": "Click"
    }


@pytest.fixture(scope='session', autouse=True)
def license_strings():
    return {
        'MIT license': 'MIT ',
        'BSD license': 'Redistributions of source code must retain the above copyright notice, this',  # noqa
        'ISC license': 'ISC License',
        'Apache Software License 2.0': 'Licensed under the Apache License, Version 2.0', # noqa
        'GNU General Public License v3': 'GNU GENERAL PUBLIC LICENSE',
    }


@contextmanager
def inside_dir(dirpath):
    """
    Execute code from inside the given directory
    :param dirpath: String, path of the directory the command is being run.
    """
    old_path = os.getcwd()
    try:
        os.chdir(dirpath)
        yield
    finally:
        os.chdir(old_path)


def assert_file_contains(file_path, *contains):
    if len(contains) == 0:
        return

    with io.open(file_path, encoding='utf-8') as _file:
        _content = _file.read()

        for _ in contains:
            assert _ in _content


def assert_file_not_contains(file_path, *not_contains):
    if len(not_contains) == 0:
        return

    with io.open(file_path, encoding='utf-8') as _file:
        _content = _file.read()

        for _ in not_contains:
            assert _ not in _content


def assert_dir_contains_file(dir_path, *file_names):
    for _ in file_names:
        assert os.path.exists(os.path.join(dir_path, _))


def test_prepare_with_default_context(tmpdir, runner, license_strings,
                                      default_context):
    default_project_slug = default_context['project_short_name']

    with inside_dir(str(tmpdir)):
        result = runner.invoke(pycake.cli, args='prepare')

        assert result.exit_code == 0
        assert os.path.isdir(default_project_slug)

        for root, dirs, files in os.walk(default_project_slug):
            for _ in files:
                assert_file_not_contains(
                    os.path.join(root, _),
                    '{{',
                    '}}'
                )

        assert_dir_contains_file(
            default_project_slug,
            *('AUTHORS.rst', 'LICENSE', '.gitignore', 'HISTORY.rst',
              'Makefile', 'MANIFEST.in', 'Pipfile', 'README.rst',
              'setup.cfg', 'tox.ini')
        )
        assert_file_contains(
            os.path.join(default_project_slug, 'setup.py'),
            default_context['author_name'],
            default_context['author_email'],
            default_context['project_repo_url'],
            license_strings['MIT license']
        )

        assert os.path.exists(
            os.path.join(
                default_project_slug, 'src', default_project_slug, 'cli.py'
            )
        )
        assert_file_contains(
            os.path.join(
                default_project_slug, 'src', default_project_slug, 'meta.py'
            ),
            default_context['author_name'],
            default_context['author_email'],
            default_context['version'],
        )


def test_prepare_with_specific_slug(tmpdir, runner, default_context):
    target_slug = 'example'
    with inside_dir(str(tmpdir)):
        result = runner.invoke(
            pycake.cli,
            args='prepare',
            input='\n\n{}\n'.format(target_slug)
        )

        assert result.exit_code == 0
        assert os.path.isdir(target_slug)

        assert_file_contains(
            os.path.join(target_slug, 'setup.py'),
            target_slug
        )


def test_prepare_without_author_file(tmpdir, runner, default_context):
    default_project_slug = default_context['project_short_name']
    with inside_dir(str(tmpdir)):
        result = runner.invoke(
            pycake.cli,
            args='prepare',
            input='\n\n\n\n\n\n\nn\n'
        )

        assert result.exit_code == 0
        assert not os.path.exists(
            os.path.join(default_project_slug, 'AUTHORS.rst')
        )


def test_prepare_not_opensource(tmpdir, runner, default_context):
    default_project_slug = default_context['project_short_name']
    with inside_dir(str(tmpdir)):
        result = runner.invoke(
            pycake.cli,
            args='prepare',
            input='\n\n\n\n\n\n\n\n6\n'
        )

        assert result.exit_code == 0
        assert_file_not_contains(
            os.path.join(default_project_slug, 'setup.py'),
            'License'
        )
        assert not os.path.exists(
            os.path.join(default_project_slug, 'LICENSE')
        )


def test_prepare_without_cli(tmpdir, runner, default_context):
    default_project_slug = default_context['project_short_name']
    with inside_dir(str(tmpdir)):
        result = runner.invoke(
            pycake.cli,
            args='prepare',
            input='\n\n\n\n\n\n\n\n\n2\n'
        )

        assert result.exit_code == 0
        assert not os.path.exists(
            os.path.join(
                default_project_slug, 'src', default_project_slug, 'cli.py'
            )
        )


def test_pycake_format_help(tmpdir, runner):
    with inside_dir(str(tmpdir)):
        result = runner.invoke(
            pycake.cli,
        )

        assert result.exit_code == 0
        assert 'Usage:' in result.stdout


def test_pycake_help(tmpdir, runner):
    p = subprocess.Popen(['python', '-m', 'pycake'], stdout=subprocess.PIPE)
    assert 'Usage:' in str(p.communicate())
