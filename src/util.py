"""
Util functions
"""

import os
import re
from .exceptions import InputError


def validate_yml_file(file_name: str):
    """Validates yml file namne to be a
    unicode string with only underscore or dash as separator
    followed by the yml extension.

    Raises:
        - InputError
    """

    if not re.match(r'^[A-Za-z0-9_-]*.yml$', file_name):
        raise InputError(f'Invalid yml file name: "{file_name}"{os.linesep}'
                            'File name may only contain only'
                            'alphanumeric characters a-z, A-Z, 0-9, '
                            'dashes -, '
                            'and underscores _, '
                            'followed by the ".yml" extension')

def validate_project_name(project_name):
    """Validates the project namne to be a
    unicode string with only underscore or dash as separator.

    Raises:
        - InputError
    """

    if not re.match(r'^[A-Za-z0-9_-]*$', project_name):
        raise InputError(f'Invalid project name: "{project_name}"{os.linesep}'
                            'Project Name may only contain '
                            'alphanumeric characters a-z, A-Z, 0-9, '
                            'dashes -, '
                            'and underscores _')
