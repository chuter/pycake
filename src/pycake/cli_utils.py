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
    help = help.replace(
        "  release",
        str(crayons.red("  release", bold=True))
    )
    additional_help = """
Usage Examples:
   Prepare the stuff for start new Python project
   $ {0}

   Release the project as REST APP
   $ {1}

   Release the project as REST APP with Dockerfile
   $ {2}

Commands:""".format(
        crayons.green("pycake prepare"),
        crayons.red("pycake release"),
        crayons.red("pycake release --docker"),
    )
    help = help.replace("Commands:", additional_help)
    return help
