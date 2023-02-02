"""Dedicated space for `create` project command."""

import os
import click

from .base_command import BaseCommand
from ..exceptions import handle_error, InputError, IntegrityError
from ..constants import DEF_ODOO_VERSION, SUPPORTED_ODOO_VERSIONS


class CreateCommand(BaseCommand):
    """
    Class that handles specific part of creating a new Odoo development project.
    """

    custom_structure: str
    odoo_version: str

    def __init__(self, project_name, odoo_version=None) -> None:
        self.odoo_version = odoo_version or DEF_ODOO_VERSION

        super().__init__(project_name)

    @handle_error
    def init_command(self) -> None:
        """
        Init command

        Raises:
            InputError: In case of invalid value for --odoo-version
        """
        super().init_command()

        if self.odoo_version not in SUPPORTED_ODOO_VERSIONS:
            allowed = '", "'.join(SUPPORTED_ODOO_VERSIONS)
            msg = f'Invalid value "{self.odoo_version}" for --odoo-version.{os.linesep}' \
                  f'Allowed values are "{allowed}"'
            raise InputError(msg)

    @handle_error
    def execute(self) -> None:
        """
        Main function called to execute the `create` command
        """
        project_structure = self.config.get_project_structure(
            custom_structure=self.custom_structure)

        project_path = os.path.join(self.config.workspace_dir, self.project_name)

        # Check if project already exists
        if os.path.isdir(project_path):
            raise IntegrityError(
                f'A directory "{self.project_name}" already exists in "{self.config.workspace_dir}"'
            )

        green_project_name = click.style(self.project_name, fg='green')
        click.echo(f'Creating project "{green_project_name}" using '
                   f'"{self.config.structure_file}" structure '
                   f'and Odoo version {self.odoo_version}')

        os.makedirs(project_path)

        self._create_structure(project_structure, project_path)

    def _create_structure(self, struct: dict, path: str) -> None:
        """
        Recursive function that generates a folders structure based on input definition.

        Args:
            struct (dict): Structure definition
            path (str): Destination path
        """
        for key, val in struct.items():
            f_path = os.path.join(path, key)

            if val['type'] == 'file':
                with open(f_path, 'w', encoding='utf8'):
                    # Create empty file
                    pass
                continue

            os.makedirs(f_path)

            if 'childs' in val:
                self._create_structure(val.get('childs'), f_path)

    @staticmethod
    def init(cli) -> None:
        """
        Attaches the `create` command to the CLI.

        Argument:
            cli: The `cli` group function.
        """

        @cli.command(help='Create a new project')
        @click.argument('project_name', required=True)
        @click.option('-s', '--structure',
                      help='Custom project structure defined in configuration folder')
        @click.option('-v', '--odoo-version',
                      help='Version of Odoo to be checked out')
        def create(project_name: str, structure: str = None, odoo_version: str = None):
            """
            Entrypoint for the project `create` command.

            Args:
                project_name (str): Technical project name.
            """
            command = CreateCommand(project_name, odoo_version=odoo_version)
            command.custom_structure = structure
            command.execute()
