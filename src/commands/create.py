"""Dedicated space for `create` project command."""

import click
from .base_command import BaseCommand


class CreateCommand(BaseCommand):
    """
    Class that handles specific part of creating a new Odoo development project.
    """

    @staticmethod
    def init(cli) -> None:
        """
        Attaches the `create` command to the CLI.

        Argument:
            cli: The `cli` group function.
        """

        @cli.command(help='Create a new project')
        @click.argument('project_name', required=True)
        def create(project_name: str):
            """
            Entrypoint for the project `create` command.

            Args:
                project_name (str): Technical project name.
            """

            green_project_name = click.style(project_name, fg='green')
            click.echo(f'Creating project {green_project_name}')

            CreateCommand(project_name)
