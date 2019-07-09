#!/usr/bin/env python
# -*- encoding: utf-8 -*-
from __future__ import absolute_import

import click
import crayons

from .meta import __version__
from .options import CONTEXT_SETTINGS, PyCakeGroup
from .cli_utils import format_help


@click.group(cls=PyCakeGroup, invoke_without_command=True,
             context_settings=CONTEXT_SETTINGS)
@click.version_option(prog_name=crayons.yellow("pycake", bold=True),
                      version=__version__)
@click.pass_context
def cli(ctx, **kwargs):
    if ctx.invoked_subcommand is None:
        click.echo(format_help(ctx.get_help()))


@cli.command(
    short_help="Prepare all the stuff to start new Python project.",
    context_settings=dict(ignore_unknown_options=True, allow_extra_args=True),
)
@click.pass_context
def prepare(ctx, **kwargs):
    from .commands import prepare

    project_dir = prepare()

    click.echo('\n\nThe target project is: {}\n'.format(project_dir))

    click.echo('You should run follow command first: {}\n'.format(
        crayons.yellow("make init", bold=True)
    ))


@cli.command(
    short_help="Release due to .pycake",
    context_settings=dict(ignore_unknown_options=True, allow_extra_args=True),
)
@click.option('--docker', help="build Dockerfile", is_flag=True)
def release(docker, **kwargs):
    from .commands import release

    release_result = release(
        with_docker_file=docker,
        **kwargs
    )
    click.echo(release_result)


if __name__ == "__main__":
    cli()
