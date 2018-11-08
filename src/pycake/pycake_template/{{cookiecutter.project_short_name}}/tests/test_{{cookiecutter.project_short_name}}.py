#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `{{ cookiecutter.project_short_name }}` package."""

import pytest
{%- if cookiecutter.command_line_interface|lower == 'click' %}
from click.testing import CliRunner
{%- endif %}

from {{ cookiecutter.project_short_name }} import {{ cookiecutter.project_short_name }}
{%- if cookiecutter.command_line_interface|lower == 'click' %}
from {{ cookiecutter.project_short_name }} import cli
{%- endif %}


@pytest.fixture
def fake_fixture():
    """
    Sample pytest fixture.

    See more at: http://doc.pytest.org/en/latest/fixture.html
    """


def test_hello(fake_fixture):
    assert {{ cookiecutter.project_short_name }}.hello() == '{{ cookiecutter.project_short_name }}'


{%- if cookiecutter.command_line_interface|lower == 'click' %}
def test_command_line_interface():
    """Test the CLI."""
    runner = CliRunner()
    result = runner.invoke(cli.main)
    assert result.exit_code == 0
    assert '{{ cookiecutter.project_short_name }}.cli.main' in result.output
    help_result = runner.invoke(cli.main, ['--help'])
    assert help_result.exit_code == 0
    assert '--help  Show this message and exit.' in help_result.output
{%- endif %}
