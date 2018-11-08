#!/usr/bin/env python
# -*- encoding: utf-8 -*-

from click import Group, Option, echo


CONTEXT_SETTINGS = dict(help_option_names=["-h", "--help"])


class PyCakeGroup(Group):
    """Custom Group class provides formatted main help"""

    def get_help_option(self, ctx):
        from .cli_utils import format_help
        """
        Override for showing formatted main help via --help and -h options
        """
        help_options = self.get_help_option_names(ctx)
        if not help_options or not self.add_help_option:
            return

        def show_help(ctx, param, value):
            if value and not ctx.resilient_parsing:
                if not ctx.invoked_subcommand:
                    # legit main help
                    echo(format_help(ctx.get_help()))
                else:
                    # legit sub-command help
                    echo(ctx.get_help(), color=ctx.color)
                ctx.exit()

        return Option(
            help_options,
            is_flag=True,
            is_eager=True,
            expose_value=False,
            callback=show_help,
            help="Show this message and exit.",
        )
