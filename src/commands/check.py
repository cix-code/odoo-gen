import click

def init_command(cli):

    @cli.command(help='Check a project structure')
    @click.argument('project_name', required=True)
    def check(project_name):
        click.echo(click.style('Checking %s ...' % project_name, fg='yellow'))
