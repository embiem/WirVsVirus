"""Command line interface."""

import click
import pathlib
import uvicorn

from wirvsvirus.settings import settings


@click.group()
def cli():
    """Command line commands."""


@cli.command()
@click.option("--reload", is_flag=True, help="reload code when it changes")
@click.pass_context
def api(ctx, reload, **kwargs):
    """Run the API.

    All additional options and arguments are passed to the "uvicorn" command.
    The default options are loaded by climatecontrol.
    """
    from wirvsvirus.api import app

    # Note: We handle reloading ourselves since the builtin "reload" option
    # crashes when invalid syntax errors occur (which can happen quickly when
    # editing).
    if reload:
        import hupper
        reloader = hupper.start_reloader(
            "wirvsvirus.cli.cli", shutdown_interval=10, verbose=2)
        reloader.watch_files(pathlib.Path(__file__).parent.glob("**/*.py"))

    uvicorn.run(app, host=settings.host, port=settings.port)
