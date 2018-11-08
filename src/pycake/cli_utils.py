#!/usr/bin/env python
# -*- encoding: utf-8 -*-

import crayons


def format_help(help):
    """Formats the help string."""
    help = help.replace("Options:", str(crayons.white("Options:", bold=True)))
    help = help.replace(
        "Usage: pycake",
        str("Usage: {0}".format(crayons.white("pycake", bold=True)))
    )
    help = help.replace(
        "  prepare",
        str(crayons.green("  prepare", bold=True))
    )
    additional_help = """
Usage Examples:
   Prepare the stuff for start new Python project
   $ {0}

Commands:""".format(
        crayons.red("pycake prepare"),
    )
    help = help.replace("Commands:", additional_help)
    return help
