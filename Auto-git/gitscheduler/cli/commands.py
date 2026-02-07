import click
import git
from pathlib import Path
from utils.time_parser import parse_time
from core.scheduler import GitScheduler
from daemon.process import start_daemon_background

@click.command()
@click.option("-m", "--message", required=True, help="Commit message")
@click.option("-t", "--time", required=True, help="Schedule time (e.g., 30m, 2h, or YYYY-MM-DD HH:MM)")
@click.option("-b", "--branch", default="main", help="Target branch")
@click.option("-r", "--repo", default=".", help="Path to git repository (default: current directory)")
def schedule(message, time, branch, repo):
    repo_path = Path(repo).resolve()
    
    try:
        git.Repo(repo_path)
    except git.InvalidGitRepositoryError:
        click.echo(f"✗ Not a git repository: {repo_path}")
        return
    except git.NoSuchPathError:
        click.echo(f"✗ Path does not exist: {repo_path}")
        return
    
    gs = GitScheduler()
    sid = gs.add(repo_path, message, branch, parse_time(time))
    click.echo(f"✓ Scheduled #{sid} for {repo_path}")
    start_daemon_background()
    click.echo("✓ Daemon started in background")
