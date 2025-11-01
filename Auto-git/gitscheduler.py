#!/usr/bin/env python3
"""
GitScheduler - Schedule your git commits and pushes
A simple, cross-platform CLI tool to schedule git operations for later execution
Works on Windows, Linux, and macOS
"""

import os
import sys
import json
import click
from datetime import datetime, timedelta
from pathlib import Path
import git
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.date import DateTrigger
import time
import signal
import threading
import subprocess
from colorama import init, Fore, Style

# Initialize colorama for cross-platform colored output
init(autoreset=True)

# Configuration - Cross-platform compatible
CONFIG_DIR = Path.home() / '.gitscheduler'
SCHEDULE_FILE = CONFIG_DIR / 'schedules.json'
LOG_FILE = CONFIG_DIR / 'scheduler.log'
PID_FILE = CONFIG_DIR / 'daemon.pid'

# Create config directory if it doesn't exist
CONFIG_DIR.mkdir(exist_ok=True)


class GitScheduler:
    def __init__(self):
        self.schedules = self.load_schedules()
        self.scheduler = BackgroundScheduler()
        
    def load_schedules(self):
        """Load schedules from file"""
        if SCHEDULE_FILE.exists():
            try:
                with open(SCHEDULE_FILE, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except:
                return []
        return []
    
    def save_schedules(self):
        """Save schedules to file"""
        with open(SCHEDULE_FILE, 'w', encoding='utf-8') as f:
            json.dump(self.schedules, f, indent=2)
    
    def add_schedule(self, repo_path, commit_message, branch, schedule_time):
        """Add a new scheduled commit"""
        schedule_id = len(self.schedules) + 1
        
        schedule = {
            'id': schedule_id,
            'repo_path': str(repo_path),
            'commit_message': commit_message,
            'branch': branch,
            'schedule_time': schedule_time.isoformat(),
            'status': 'pending',
            'created_at': datetime.now().isoformat()
        }
        
        self.schedules.append(schedule)
        self.save_schedules()
        
        return schedule_id
    
    def remove_schedule(self, schedule_id):
        """Remove a schedule by ID"""
        self.schedules = [s for s in self.schedules if s['id'] != schedule_id]
        self.save_schedules()
    
    def execute_schedule(self, schedule_id):
        """Execute a scheduled git operation"""
        schedule = next((s for s in self.schedules if s['id'] == schedule_id), None)
        
        if not schedule:
            self.log(f"Schedule {schedule_id} not found")
            return False
        
        try:
            repo = git.Repo(schedule['repo_path'])
            
            # Check if repo is dirty (has changes)
            if repo.is_dirty(untracked_files=True):
                # Add all changes
                repo.git.add(A=True)
                
                # Commit
                repo.index.commit(schedule['commit_message'])
                
                # Push
                origin = repo.remote(name='origin')
                origin.push(schedule['branch'])
                
                # Update schedule status
                for s in self.schedules:
                    if s['id'] == schedule_id:
                        s['status'] = 'completed'
                        s['completed_at'] = datetime.now().isoformat()
                
                self.save_schedules()
                self.log(f"✓ Successfully pushed to {schedule['branch']}: {schedule['commit_message']}")
                return True
            else:
                self.log(f"⚠ No changes to commit in {schedule['repo_path']}")
                for s in self.schedules:
                    if s['id'] == schedule_id:
                        s['status'] = 'no_changes'
                self.save_schedules()
                return False
                
        except Exception as e:
            self.log(f"✗ Error executing schedule {schedule_id}: {str(e)}")
            for s in self.schedules:
                if s['id'] == schedule_id:
                    s['status'] = 'failed'
                    s['error'] = str(e)
            self.save_schedules()
            return False
    
    def log(self, message):
        """Log message to file and console"""
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        log_message = f"[{timestamp}] {message}"
        
        try:
            with open(LOG_FILE, 'a', encoding='utf-8') as f:
                f.write(log_message + '\n')
        except:
            pass
        
        print(log_message)


def is_daemon_running():
    """Check if daemon is already running"""
    if not PID_FILE.exists():
        return False
    
    try:
        with open(PID_FILE, 'r') as f:
            pid = int(f.read().strip())
        
        # Check if process is running (cross-platform)
        if sys.platform == 'win32':
            # Windows
            import ctypes
            PROCESS_QUERY_INFORMATION = 0x0400
            handle = ctypes.windll.kernel32.OpenProcess(PROCESS_QUERY_INFORMATION, False, pid)
            if handle:
                ctypes.windll.kernel32.CloseHandle(handle)
                return True
            return False
        else:
            # Linux/macOS
            try:
                os.kill(pid, 0)
                return True
            except OSError:
                return False
    except:
        return False


def start_daemon_background():
    """Start daemon in background (cross-platform)"""
    if is_daemon_running():
        click.echo(f"{Fore.YELLOW}⚠ Daemon is already running{Style.RESET_ALL}")
        return True
    
    # Get the path to current script
    script_path = os.path.abspath(__file__)
    
    if sys.platform == 'win32':
        # Windows - use subprocess with CREATE_NEW_PROCESS_GROUP
        subprocess.Popen(
            [sys.executable, script_path, 'daemon', '--background'],
            creationflags=subprocess.CREATE_NEW_PROCESS_GROUP | subprocess.DETACHED_PROCESS,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            stdin=subprocess.DEVNULL
        )
    else:
        # Linux/macOS - use nohup
        subprocess.Popen(
            ['nohup', sys.executable, script_path, 'daemon', '--background'],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            stdin=subprocess.DEVNULL,
            preexec_fn=os.setpgrp
        )
    
    time.sleep(1)  # Give daemon time to start
    return True


# CLI Commands
@click.group(invoke_without_command=True)
@click.pass_context
def cli(ctx):
    """GitScheduler - Schedule your git commits and pushes
    
    Run without arguments for interactive mode."""
    if ctx.invoked_subcommand is None:
        # Interactive mode - one prompt workflow
        interactive_mode()


def interactive_mode():
    """Interactive mode - complete workflow in one run"""
    click.echo(f"\n{Fore.CYAN}{'='*70}{Style.RESET_ALL}")
    click.echo(f"{Fore.CYAN}GitScheduler - Interactive Mode{Style.RESET_ALL}")
    click.echo(f"{Fore.CYAN}{'='*70}{Style.RESET_ALL}\n")
    
    # Check if in git repository
    try:
        repo = git.Repo('.')
        repo_path = Path('.').resolve()
        click.echo(f"{Fore.GREEN}✓ Git repository detected: {repo_path}{Style.RESET_ALL}\n")
    except git.exc.InvalidGitRepositoryError:
        click.echo(f"{Fore.RED}✗ Not a git repository!{Style.RESET_ALL}")
        click.echo(f"Please run this command from inside a git repository.\n")
        return
    
    # Show menu
    click.echo(f"{Fore.YELLOW}What would you like to do?{Style.RESET_ALL}")
    click.echo("1. Schedule a new commit")
    click.echo("2. List all schedules")
    click.echo("3. Cancel a schedule")
    click.echo("4. View logs")
    click.echo("5. Clear completed schedules")
    click.echo("6. Exit")
    
    choice = click.prompt("\nEnter your choice", type=int, default=1)
    
    if choice == 1:
        # Schedule workflow
        click.echo(f"\n{Fore.CYAN}--- Schedule a Commit ---{Style.RESET_ALL}\n")
        
        # Get commit message
        message = click.prompt("Commit message", type=str)
        
        # Get time
        click.echo("\nTime format examples:")
        click.echo("  - 30m (30 minutes from now)")
        click.echo("  - 2h (2 hours from now)")
        click.echo("  - 2025-11-01 18:30 (specific date and time)")
        time_input = click.prompt("Schedule time", type=str, default="30m")
        
        # Get branch
        try:
            current_branch = repo.active_branch.name
            branch = click.prompt("Branch name", type=str, default=current_branch)
        except:
            branch = click.prompt("Branch name", type=str, default="main")
        
        # Parse time
        try:
            if time_input.endswith('m'):
                minutes = int(time_input[:-1])
                schedule_time = datetime.now() + timedelta(minutes=minutes)
            elif time_input.endswith('h'):
                hours = int(time_input[:-1])
                schedule_time = datetime.now() + timedelta(hours=hours)
            else:
                schedule_time = datetime.strptime(time_input, '%Y-%m-%d %H:%M')
        except ValueError:
            click.echo(f"\n{Fore.RED}✗ Invalid time format{Style.RESET_ALL}")
            return
        
        if schedule_time <= datetime.now():
            click.echo(f"\n{Fore.RED}✗ Schedule time must be in the future{Style.RESET_ALL}")
            return
        
        # Add schedule
        gs = GitScheduler()
        schedule_id = gs.add_schedule(repo_path, message, branch, schedule_time)
        
        click.echo(f"\n{Fore.GREEN}✓ Successfully scheduled commit #{schedule_id}{Style.RESET_ALL}")
        click.echo(f"  Message: {message}")
        click.echo(f"  Branch: {branch}")
        click.echo(f"  Time: {schedule_time.strftime('%Y-%m-%d %H:%M:%S')}")
        
        # Ask to start daemon
        click.echo(f"\n{Fore.YELLOW}The daemon needs to run for the schedule to execute.{Style.RESET_ALL}")
        start_now = click.confirm("Start daemon now?", default=True)
        
        if start_now:
            click.echo(f"\n{Fore.CYAN}Starting daemon...{Style.RESET_ALL}")
            if start_daemon_background():
                click.echo(f"{Fore.GREEN}✓ Daemon started successfully!{Style.RESET_ALL}")
                click.echo(f"Your commit will be pushed automatically at the scheduled time.")
            else:
                click.echo(f"{Fore.YELLOW}Note: Run 'python gitscheduler.py daemon' manually if needed{Style.RESET_ALL}")
        
    elif choice == 2:
        # List schedules
        list_schedules()
        
    elif choice == 3:
        # Cancel schedule
        list_schedules()
        schedule_id = click.prompt("\nEnter schedule ID to cancel", type=int)
        cancel_schedule(schedule_id)
        
    elif choice == 4:
        # View logs
        view_logs()
        
    elif choice == 5:
        # Clear schedules
        clear_schedules()
        
    else:
        click.echo("\nGoodbye!")


def list_schedules():
    """List all scheduled commits"""
    gs = GitScheduler()
    
    if not gs.schedules:
        click.echo(f"\n{Fore.YELLOW}No scheduled commits{Style.RESET_ALL}\n")
        return
    
    click.echo(f"\n{Fore.CYAN}{'='*70}{Style.RESET_ALL}")
    click.echo(f"{Fore.CYAN}Scheduled Commits{Style.RESET_ALL}")
    click.echo(f"{Fore.CYAN}{'='*70}{Style.RESET_ALL}\n")
    
    for schedule in gs.schedules:
        status_color = {
            'pending': Fore.YELLOW,
            'completed': Fore.GREEN,
            'failed': Fore.RED,
            'no_changes': Fore.BLUE
        }.get(schedule['status'], Fore.WHITE)
        
        click.echo(f"ID: {Fore.CYAN}{schedule['id']}{Style.RESET_ALL}")
        click.echo(f"  Status: {status_color}{schedule['status'].upper()}{Style.RESET_ALL}")
        click.echo(f"  Message: {schedule['commit_message']}")
        click.echo(f"  Branch: {schedule['branch']}")
        click.echo(f"  Repository: {schedule['repo_path']}")
        click.echo(f"  Scheduled: {schedule['schedule_time']}")
        
        if schedule['status'] == 'failed' and 'error' in schedule:
            click.echo(f"  Error: {Fore.RED}{schedule['error']}{Style.RESET_ALL}")
        
        click.echo()


def cancel_schedule(schedule_id):
    """Cancel a schedule"""
    gs = GitScheduler()
    
    schedule = next((s for s in gs.schedules if s['id'] == schedule_id), None)
    
    if not schedule:
        click.echo(f"\n{Fore.RED}✗ Schedule #{schedule_id} not found{Style.RESET_ALL}\n")
        return
    
    if schedule['status'] != 'pending':
        click.echo(f"\n{Fore.RED}✗ Cannot cancel a {schedule['status']} schedule{Style.RESET_ALL}\n")
        return
    
    gs.remove_schedule(schedule_id)
    click.echo(f"\n{Fore.GREEN}✓ Cancelled schedule #{schedule_id}{Style.RESET_ALL}\n")


def clear_schedules():
    """Clear completed/failed schedules"""
    gs = GitScheduler()
    original_count = len(gs.schedules)
    gs.schedules = [s for s in gs.schedules if s['status'] == 'pending']
    gs.save_schedules()
    removed = original_count - len(gs.schedules)
    click.echo(f"\n{Fore.GREEN}✓ Removed {removed} completed/failed schedules{Style.RESET_ALL}\n")


def view_logs():
    """View logs"""
    if LOG_FILE.exists():
        with open(LOG_FILE, 'r', encoding='utf-8') as f:
            content = f.read()
            if content:
                click.echo(f"\n{Fore.CYAN}{'='*70}{Style.RESET_ALL}")
                click.echo(f"{Fore.CYAN}Scheduler Logs{Style.RESET_ALL}")
                click.echo(f"{Fore.CYAN}{'='*70}{Style.RESET_ALL}\n")
                click.echo(content)
            else:
                click.echo(f"\n{Fore.YELLOW}No logs yet{Style.RESET_ALL}\n")
    else:
        click.echo(f"\n{Fore.YELLOW}No logs yet{Style.RESET_ALL}\n")


@cli.command()
@click.option('--message', '-m', required=True, help='Commit message')
@click.option('--time', '-t', required=True, help='Schedule time (e.g., "2025-11-01 18:30" or "30m" for 30 minutes)')
@click.option('--branch', '-b', default='main', help='Branch name (default: main)')
@click.option('--path', '-p', default='.', help='Repository path (default: current directory)')
@click.option('--auto-start', '-a', is_flag=True, help='Automatically start daemon after scheduling')
def schedule(message, time, branch, path, auto_start):
    """Schedule a commit and push"""
    
    # Parse time
    try:
        if time.endswith('m'):
            minutes = int(time[:-1])
            schedule_time = datetime.now() + timedelta(minutes=minutes)
        elif time.endswith('h'):
            hours = int(time[:-1])
            schedule_time = datetime.now() + timedelta(hours=hours)
        else:
            schedule_time = datetime.strptime(time, '%Y-%m-%d %H:%M')
    except ValueError:
        click.echo(f"{Fore.RED}✗ Invalid time format. Use 'YYYY-MM-DD HH:MM' or '30m' or '2h'{Style.RESET_ALL}")
        return
    
    if schedule_time <= datetime.now():
        click.echo(f"{Fore.RED}✗ Schedule time must be in the future{Style.RESET_ALL}")
        return
    
    # Verify git repository
    try:
        repo = git.Repo(path)
    except git.exc.InvalidGitRepositoryError:
        click.echo(f"{Fore.RED}✗ Not a git repository: {path}{Style.RESET_ALL}")
        return
    
    # Add schedule
    gs = GitScheduler()
    schedule_id = gs.add_schedule(Path(path).resolve(), message, branch, schedule_time)
    
    click.echo(f"{Fore.GREEN}✓ Scheduled commit #{schedule_id}{Style.RESET_ALL}")
    click.echo(f"  Message: {message}")
    click.echo(f"  Branch: {branch}")
    click.echo(f"  Time: {schedule_time.strftime('%Y-%m-%d %H:%M:%S')}")
    
    if auto_start:
        click.echo(f"\n{Fore.CYAN}Starting daemon...{Style.RESET_ALL}")
        start_daemon_background()
    else:
        click.echo(f"\n{Fore.YELLOW}Run 'python gitscheduler.py daemon' to start the scheduler{Style.RESET_ALL}")


@cli.command()
def list():
    """List all scheduled commits"""
    list_schedules()


@cli.command()
@click.argument('schedule_id', type=int)
def cancel(schedule_id):
    """Cancel a scheduled commit"""
    cancel_schedule(schedule_id)


@cli.command()
def clear():
    """Clear all completed/failed schedules"""
    clear_schedules()


@cli.command()
@click.option('--background', is_flag=True, hidden=True, help='Run in background mode')
def daemon(background):
    """Run the scheduler daemon (keeps running to execute scheduled tasks)"""
    gs = GitScheduler()
    
    # Save PID
    with open(PID_FILE, 'w') as f:
        f.write(str(os.getpid()))
    
    gs.scheduler.start()
    
    # Add all pending schedules
    pending_count = 0
    for schedule in gs.schedules:
        if schedule['status'] == 'pending':
            schedule_time = datetime.fromisoformat(schedule['schedule_time'])
            if schedule_time > datetime.now():
                gs.scheduler.add_job(
                    gs.execute_schedule,
                    DateTrigger(run_date=schedule_time),
                    args=[schedule['id']],
                    id=f"schedule_{schedule['id']}"
                )
                pending_count += 1
    
    if not background:
        click.echo(f"{Fore.GREEN}✓ GitScheduler daemon started{Style.RESET_ALL}")
        click.echo(f"  Monitoring {pending_count} pending schedules")
        click.echo(f"  Log file: {LOG_FILE}")
        click.echo(f"\n{Fore.YELLOW}Press Ctrl+C to stop{Style.RESET_ALL}\n")
    
    # Handle graceful shutdown
    def signal_handler(sig, frame):
        if not background:
            click.echo(f"\n{Fore.YELLOW}Shutting down scheduler...{Style.RESET_ALL}")
        gs.scheduler.shutdown()
        if PID_FILE.exists():
            PID_FILE.unlink()
        sys.exit(0)
    
    signal.signal(signal.SIGINT, signal_handler)
    if sys.platform != 'win32':
        signal.signal(signal.SIGTERM, signal_handler)
    
    try:
        while True:
            time.sleep(1)
    except (KeyboardInterrupt, SystemExit):
        gs.scheduler.shutdown()
        if PID_FILE.exists():
            PID_FILE.unlink()


@cli.command()
def logs():
    """View scheduler logs"""
    view_logs()


@cli.command()
def status():
    """Check if daemon is running"""
    if is_daemon_running():
        click.echo(f"{Fore.GREEN}✓ Daemon is running{Style.RESET_ALL}")
    else:
        click.echo(f"{Fore.YELLOW}⚠ Daemon is not running{Style.RESET_ALL}")
        click.echo(f"Run 'python gitscheduler.py daemon' to start it")


if __name__ == '__main__':
    cli()