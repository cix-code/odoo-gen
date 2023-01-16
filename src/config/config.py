"""
Config definition of oCLI
"""

import os
import configparser
import click

from ..constants import APP_NAME
from ..exceptions import UserAbortError, ConfigError


class Config:
    """
    Config class provide useful functions to read and store configuration values
    oCLI stores an ocli.conf file in user's default configuration folder
    """

    conf_path = False

    # Config values
    workspace_dir = False

    def __init__(self) -> None:

        app_path = click.get_app_dir(APP_NAME)
        if not os.path.isdir(app_path):
            os.makedirs(app_path)

        self.conf_path = self._get_conf_path()

        self.load_config()

    @staticmethod
    def _get_conf_path() -> str:
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
        Loads the config values from the config file.
        Creates the config file if it doesn't exist.
        """

        # Create new config file with default values if no config exists yet
        if not os.path.exists(self.conf_path):
            click.echo('Configuration file not found. Attempting to create it.')
            self.load_default_values()
            self.store_config_file()

        config = configparser.ConfigParser()

        try:
            config.read(self.conf_path)
        except configparser.Error as err:
            raise ConfigError(err.message) from err

    def load_default_values(self) -> None:
        "Sets default config values"

        self.workspace_dir = os.getcwd()

        click.echo(
            f'The following will be your workspace directory: {self.workspace_dir}')

        # Get user's confirmation to use current path as workspace folder
        cont = click.confirm('Continue?', default=True)
        if not cont:
            important = click.style('Important!', fg='red')
            raise UserAbortError(f'{important} Execute the `ocli` command in the '
                                 'folder that will be your workspace.')

    def store_config_file(self) -> None:
        """
        Stores the configuration in a config file
        """

        config = configparser.ConfigParser()

        config['Workspace'] = {
            'workspace_dir': self.workspace_dir,
        }

        # Create a new section
        config['Projects'] = {}

        # Save the config file
        with open(self.conf_path, 'w', encoding='utf8') as conf_file:
            conf_file.writelines([
                f'# This is the configuration file for oCLI{os.linesep}',
                f'# Do not change this file manually{os.linesep}',
                os.linesep
            ])
            config.write(conf_file)
