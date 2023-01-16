"""Common part of all `commands` that oCLI can execute"""

import os
import re
import sys

from ..config.config import Config
from ..exceptions import OCLIError, InputError


class BaseCommand:
    """Abstract class inherited by all commands of oCLI"""

    config = False
    project_name = False

    def __init__(self, project_name) -> None:
        self.project_name = project_name

        try:
            self._validate_project_name()

            self.load_config()

        except OCLIError as err:
            err.display_details()
            if err.abort:
                sys.exit(1)

    def load_config(self) -> None:
        """Loads configuration"""

        self.config = Config()

    def _validate_project_name(self):
        """Validates the project namne to be a
        unicode string with only underscore or dash as separator.
        """

        if not re.match(r'^[A-Za-z0-9_-]*$', self.project_name):
            raise InputError(f'Invalid project name: "{self.project_name}"{os.linesep}'
                             'Project Name may only contain '
                             'alphanumeric characters a-z, A-Z, 0-9, '
                             'dashes -, '
                             'and underscores _')

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
