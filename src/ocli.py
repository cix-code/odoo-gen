"""
oCLI - odoo Command Line Interface - Helper tool for developers working on multiple odoo projects
"""

import click

from .commands.create import CreateCommand
from .commands.control import ControlCommand
# from .commands.check import CheckCommand
# from .commands.remove import RemoveCommand

from .constants import VERSION


@click.group(no_args_is_help=True, invoke_without_command=True)
@click.option('-v', '--version', flag_value=True, help='Show installed version of ocli')
def cli(version=False):
    """
    CLI definition as group of commands.
    Running oCLI without a command will trigger the help info.
    """
    if version:
        click.echo(f'ocli version {VERSION}')


CreateCommand.init(cli)
ControlCommand.init(cli)

# CheckCommand.init(cli)
# RemoveCommand.init(cli)
