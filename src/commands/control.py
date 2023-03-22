"""Dedicated space for start, restart, stop, etc commands."""

import click

from ..models.abstract.base_command import BaseCommand
from ..models.project import Project
from ..exceptions import handle_error
from ..exceptions import ConfigError


class ControlCommand(BaseCommand):
    """
    Class that handles specific commands of controlling project's activity.
    """

    project: Project
    mode: str = 'control'

    @handle_error
    def __init__(self, project_name: str = ''):  # pylint: disable=unused-argument
        super().__init__()

        project_name = project_name or self.get_config('active_project')
        if not project_name:
            raise ConfigError(
                f'No `active_project` found in {self._config_file_path}')

        self.project = Project(
            command=self,
            project_data={
                'project_name': project_name
            })

    @handle_error
    def start(self) -> None:
        """
        Function called to execute the `start` command
        """
        self.project.start()
        self.save_config()

    @handle_error
    def stop(self) -> None:
        """
        Function called to execute the `stop` command
        """
        self.project.stop()
        self.save_config()

    @handle_error
    def restart(self) -> None:
        """
        Function called to execute the `restart` command
        """
        self.project.restart()
        self.save_config()

    @staticmethod
    def init(cli) -> None:
        """
        Attaches the `start`, `stop`, `restart` commands to the CLI.

        Argument:
            cli: The `cli` group function.
        """

        @cli.command(help='Starts the docker containers for the active project')
        @click.argument('project_name', required=False)
        def start(project_name: str = '') -> None:
            """
            Entrypoint for the project `start` command.

            Args:
                project_name (str): Optional: Technical project name.
            """
            command = ControlCommand(
                project_name=project_name
            )
            command.start()

        @cli.command(help='Stops the docker containers for the active project')
        def stop() -> None:
            """
            Entrypoint for the project `stop` command.
            """
            command = ControlCommand()
            command.stop()

        @cli.command(help='Restarts the docker containers for the active project')
        def restart() -> None:
            """
            Entrypoint for the project `restart` command.
            """
            command = ControlCommand()
            command.restart()
