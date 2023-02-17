"""
Helper functions
"""

import os
import re
import subprocess
import selectors
import random
import string
import click

from ..exceptions import InputError, OCLIError


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


def execute_command(command: list) -> None:
    """
    Executes a command and outputs its stdout and stderr to the console.

    Args:
        command (list): List of the command and args ready to be passed to subprocess.Popen
    """
    def read_output(file, mask):  # pylint: disable=unused-argument
        line = file.readline().decode("utf-8").strip()
        if line:
            click.echo(line)

    sel = selectors.DefaultSelector()

    with subprocess.Popen(command,
                          stdout=subprocess.PIPE,
                          stderr=subprocess.PIPE) as process:

        if process.stdout:
            sel.register(process.stdout, selectors.EVENT_READ, read_output)
        if process.stderr:
            sel.register(process.stderr, selectors.EVENT_READ, read_output)

        while process.poll() is None:
            events = sel.select()
            for key, mask in events:
                callback = key.data
                callback(key.fileobj, mask)

        if process.returncode != 0 and process.stderr:
            err = process.stderr.readline().decode("utf-8").strip()
            raise OCLIError(f'Cloning repository failed.{os.linesep}{err}')


def generate_password(length=20) -> str:
    """
    Generates a random password of specified length

    Args:
        length (int, optional): Desired length. Defaults to 20.

    Returns:
        str: Generated password.
    """
    source = string.ascii_lowercase + \
        string.ascii_uppercase + \
        string.digits

    return ''.join([random.choice(source) for i in range(0, length)])
