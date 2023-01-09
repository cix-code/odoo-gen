import click


def init_command(cli):

    @cli.command(help='Create a new project')
    @click.argument('project_name', required=True)
    def create(project_name):
        pass
