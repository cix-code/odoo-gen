"""Common part of all `commands` that oCLI can execute"""

import os
import click

from .base_config import BaseConfig
from ...constants import APP_NAME
from ...exceptions import handle_error
from ...exceptions import UserAbortError


class BaseCommand(BaseConfig):
    """Abstract class inherited by all commands of oCLI"""

    mode: str

    def __init__(self) -> None:
        # Init config
        app_path = click.get_app_dir(APP_NAME)

        self._config_path = app_path
        self._config_file = 'ocli.conf'
        self._config_header = f'# This is the configuration file for oCLI{os.linesep}' \
            f'# Do not change this file manually{os.linesep}{os.linesep}'

        super().__init__()

    def get_default_config(self) -> dict:
        workspace_dir = os.getcwd()
        click.echo(
            f'The following will be your workspace directory: {workspace_dir}')

        # Get user's confirmation to use current path as workspace folder
        cont = click.confirm('Continue?', default=True)
        if not cont:
            important = click.style('Important!', fg='red')
            raise UserAbortError(f'{important} Execute the `ocli` command in the '
                                 'folder that will be your workspace.')

        return {
            'DEFAULT': {
                'workspace_dir': workspace_dir,
                'active_project': ''
            }
        }

    @property
    def conf_dir(self) -> str:
        """
        Gets the path to the config folder.

        Returns:
            str: The path.
        """
        return self._config_path

    @handle_error
    def execute(self) -> None:
        """Main function called to execute a command"""

    @staticmethod
    def init(cli) -> None:
        """
        Abstract definition for the `init` function.
        It is responsible for attaching the command to the oCLI.

        Argument:
            cli: The `cli` group function.

        Raises:
            NotImplementedError: This should never be reached
        """
        raise NotImplementedError()
