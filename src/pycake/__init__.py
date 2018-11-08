#!/usr/bin/env python
# -*- encoding: utf-8 -*-

# flake8: noqa

from .meta import __version__
from .cli import cli

if __name__ == "__main__":   # pragma: no cover
    cli()
