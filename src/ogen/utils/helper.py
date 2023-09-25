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

from subprocess import PIPE, STDOUT

from ..constants import SUPPORTED_ODOO_VERSIONS
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


def validate_project_name(project_name: str):
    """Validates the project namne to be a
    unicode string with only underscore or dash as separator.

    Raises:
        - InputError
    """
    err = ''
    if len(project_name) > 32:
        err += os.linesep + 'Project Name may not exceed 32 characters'

    if not re.match(r'^[A-Za-z0-9_-]*$', project_name):
        err += os.linesep + \
            'Project Name may only contain ' \
            'alphanumeric characters a-z, A-Z, 0-9, ' \
            'dashes -, ' \
            'and underscores _'
    if err:
        raise InputError(f'Invalid project name: "{project_name}"' + err)


def validate_odoo_version(version: str):
    """
    _summary_

    Args:
        version (str): _description_
    """
    if version not in SUPPORTED_ODOO_VERSIONS:
        allowed = '", "'.join(SUPPORTED_ODOO_VERSIONS)
        msg = f'Invalid value "{version}" for --odoo-version.{os.linesep}' \
              f'Allowed values are "{allowed}"'
        raise InputError(msg)


def execute_command(command: list,
                    allow_error: bool = False,
                    return_output: bool = False) -> str|bool:
    if return_output:
        return subprocess.check_output(command, encoding="utf8").strip()
    try:
        subprocess.check_call(command)
    except subprocess.CalledProcessError as err:
        if allow_error:
            return False
        raise OCLIError(f'Error executing the command.{os.linesep}{err}') \
            from err
    return True

def execute_command_old(command: list,
                    allow_error: bool = False,
                    return_output: bool = False) -> str:
    """
    Executes a command and outputs its stdout and stderr to the console.

    Args:
        command (list): List of the command and args ready to be passed to subprocess.Popen
    """
    output = ''
    sep = ''

    def read_output(file, mask):  # pylint: disable=unused-argument
        line = file.readline().decode("utf-8").strip()
        if not line:
            return None
        if return_output:
            return line
        return click.echo(line)

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
                line = callback(key.fileobj, mask)
                if return_output and line:
                    output += sep + line
                    sep = os.linesep

        if process.returncode != 0 and process.stderr:
            err = process.stderr.readline().decode("utf-8").strip()
            if not allow_error:
                raise OCLIError(
                    f'Error executing the command.{os.linesep}{err}')

        # Sometimes a part of the output remains in process.stdout
        # and it's not processed by read_output handler,
        # therefore this 'hack' is needed
        if process.stdout:
            remaining_output = process.stdout.read().decode("utf-8").strip()
            if return_output:
                output += sep + remaining_output
            else:
                click.echo(output)

    return output

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
