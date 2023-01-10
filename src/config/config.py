"""
Config definition of oCLI
"""

import os
import configparser
import click

from ..constants import APP_NAME
from ..exceptions import UserAbortException


class Config:
    """
    Config class provide useful functions to read and store configuration values
    oCLI stores an ocli.conf file in user's default configuration folder
    """

    conf_path = False
    base_path = False

    def __init__(self) -> None:

        app_path = click.get_app_dir(APP_NAME)
        if not os.path.isdir(app_path):
            os.makedirs(app_path)

        self.conf_path = self._prepare_conf_path()

        self.load_config()

    @staticmethod
    def _prepare_conf_path() -> str:
        """
        Prepares the conf file path.
        If the app folder doesn't exist, it gets created.

        Returns:
            str: The full path to the config file.
        """

        app_path = click.get_app_dir(APP_NAME)
        if not os.path.isdir(app_path):
            os.makedirs(app_path)

        return os.path.join(app_path, 'ocli.conf')

    def load_config(self) -> None:
        """
        Loads or create default configuration file
        """

        if not os.path.exists(self.conf_path):
            click.echo('Configuration file not found. Attempting to create it.')
            self.store_default_config()

        print(f'Loading config from {self.conf_path}')

    def store_default_config(self) -> None:
        """
        Generates a new config file and populates it with default values
        """

        config = configparser.ConfigParser()

        workspace_path = os.getcwd()

        click.echo(f'The following will be your workspace directory: {workspace_path}')

        cont = click.confirm('Continue?', default=True)
        if not cont:
            click.echo(
                'Execute the first `ocli` command in the ' \
                'folder that will be your workspace.')
            raise UserAbortException()

        # Set default values
        config['Workspace'] = {
            'workspace_dir': os.getcwd(),
        }

        # Create a new section
        config['Projects'] = {}

        # Save the config file
        with open(self.conf_path, 'w', encoding='utf8') as conf_file:
            config.write(conf_file)
