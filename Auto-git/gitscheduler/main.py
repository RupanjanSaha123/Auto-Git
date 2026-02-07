import click
from cli.commands import schedule
from cli.interactive import interactive_mode
from daemon.runner import run_daemon
from daemon.process import is_running

@click.group(invoke_without_command=True)
@click.pass_context
def cli(ctx):
    if ctx.invoked_subcommand is None:
        interactive_mode()

@cli.command()
def daemon():
    run_daemon()

@cli.command()
def status():
    click.echo("Running" if is_running() else "Not running")

cli.add_command(schedule)

if __name__ == "__main__":
    cli()
