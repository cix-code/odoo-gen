"""
Custom Exceptions
"""

import click


class OCLIError(BaseException):
    "Abstract oCLI Exception"

    message = 'Unexpected Error'
    details = 'Command terminated due to a configuration error.'
    abort = True

    def __init__(self, message, *args: object) -> None:
        self.message = message
        super().__init__(*args)

    def display_details(self) -> None:
        """
        Outputs the error details to the terminal
        """

        click.echo(self.message)
        click.echo(self.details)

class UserAbortError(OCLIError):
    """
    Exception raised when the user decides to abort.
    """
    details = 'Command terminated by user.'

class ConfigError(OCLIError):
    """
    Exception raised when configuration is invalid.
    """
    details = 'Command terminated due to a configuration error.'

class InputError(OCLIError):
    """
    Exception raised when user provides invalid input.
    """
    details = 'Command terminated due to an invalid input.'
