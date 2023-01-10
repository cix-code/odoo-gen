"""Common part of all `commands` that oCLI can execute"""

import click

from ..config.config import Config
from ..exceptions import UserAbortException


class BaseCommand:
    """Abstract class inherited by all commands of oCLI"""

    config = False
    project_name = False

    def __init__(self, project_name) -> None:
        self.project_name = project_name

        try:
            self._validate_project_name()

            self.load_config()

        except UserAbortException:
            click.echo('Command terminated by user.')

    def load_config(self) -> None:
        """Loads configuration"""

        self.config = Config()


    def _validate_project_name(self):
        """Validates the project namne to be a
        unicode string with only underscore or dash as separator.
        """

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
