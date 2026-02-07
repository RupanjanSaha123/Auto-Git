import click, git
from pathlib import Path
from utils.time_parser import parse_time
from core.scheduler import GitScheduler
from daemon.process import start_daemon_background

def interactive_mode():
    repo_input = click.prompt("Repository path", default=".", show_default=True)
    repo_path = Path(repo_input).resolve()
    
    try:
        git.Repo(repo_path)
    except git.InvalidGitRepositoryError:
        click.echo(f"✗ Not a git repository: {repo_path}")
        return
    except git.NoSuchPathError:
        click.echo(f"✗ Path does not exist: {repo_path}")
        return

    msg = click.prompt("Commit message")
    t = click.prompt("Schedule time", default="30m")
    branch = click.prompt("Branch", default="main")

    gs = GitScheduler()
    sid = gs.add(repo_path, msg, branch, parse_time(t))
    click.echo(f"✓ Scheduled #{sid} for {repo_path}")
    start_daemon_background()
    click.echo("✓ Daemon started in background")
