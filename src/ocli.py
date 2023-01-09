import click

from .commands import create
from .commands import check
from .commands import remove
from .constants import version as ocli_version


@click.group(no_args_is_help=True, invoke_without_command=True)
@click.option('-v', '--version', flag_value=True, help='Show installed version of ocli')
def cli(version=False):
    print("version %s" % ocli_version)
    pass


create.init_command(cli)
check.init_command(cli)
remove.init_command(cli)
