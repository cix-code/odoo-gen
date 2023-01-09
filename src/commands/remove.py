import click

def init_command(cli):

    @cli.command(help='Remove a project')
    @click.argument('project_name', required=True)
    def remove(project_name):
        click.echo(click.style('Removing %s ...' % project_name, fg='red'))