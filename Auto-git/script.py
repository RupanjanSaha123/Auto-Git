
# Let's create the complete CLI tool structure for GitScheduler

# First, let's create the requirements.txt content
requirements_txt = """gitpython==3.1.40
apscheduler==3.10.4
click==8.1.7
python-dateutil==2.8.2
colorama==0.4.6
"""

# Main CLI application code
main_code = """#!/usr/bin/env python3
\"\"\"
GitScheduler - Schedule your git commits and pushes
A simple CLI tool to schedule git operations for later execution
\"\"\"

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
from colorama import init, Fore, Style

# Initialize colorama for cross-platform colored output
init(autoreset=True)

# Configuration
CONFIG_DIR = Path.home() / '.gitscheduler'
SCHEDULE_FILE = CONFIG_DIR / 'schedules.json'
LOG_FILE = CONFIG_DIR / 'scheduler.log'

# Create config directory if it doesn't exist
CONFIG_DIR.mkdir(exist_ok=True)


class GitScheduler:
    def __init__(self):
        self.schedules = self.load_schedules()
        self.scheduler = BackgroundScheduler()
        
    def load_schedules(self):
        \"\"\"Load schedules from file\"\"\"
        if SCHEDULE_FILE.exists():
            with open(SCHEDULE_FILE, 'r') as f:
                return json.load(f)
        return []
    
    def save_schedules(self):
        \"\"\"Save schedules to file\"\"\"
        with open(SCHEDULE_FILE, 'w') as f:
            json.dump(self.schedules, f, indent=2)
    
    def add_schedule(self, repo_path, commit_message, branch, schedule_time):
        \"\"\"Add a new scheduled commit\"\"\"
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
        \"\"\"Remove a schedule by ID\"\"\"
        self.schedules = [s for s in self.schedules if s['id'] != schedule_id]
        self.save_schedules()
    
    def execute_schedule(self, schedule_id):
        \"\"\"Execute a scheduled git operation\"\"\"
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
        \"\"\"Log message to file and console\"\"\"
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        log_message = f"[{timestamp}] {message}"
        
        with open(LOG_FILE, 'a') as f:
            f.write(log_message + '\\n')
        
        print(log_message)


# CLI Commands
@click.group()
def cli():
    \"\"\"GitScheduler - Schedule your git commits and pushes\"\"\"
    pass


@cli.command()
@click.option('--message', '-m', required=True, help='Commit message')
@click.option('--time', '-t', required=True, help='Schedule time (e.g., "2025-10-25 14:30" or "30m" for 30 minutes)')
@click.option('--branch', '-b', default='main', help='Branch name (default: main)')
@click.option('--path', '-p', default='.', help='Repository path (default: current directory)')
def schedule(message, time, branch, path):
    \"\"\"Schedule a commit and push\"\"\"
    
    # Parse time
    try:
        if time.endswith('m'):
            # Relative time in minutes
            minutes = int(time[:-1])
            schedule_time = datetime.now() + timedelta(minutes=minutes)
        elif time.endswith('h'):
            # Relative time in hours
            hours = int(time[:-1])
            schedule_time = datetime.now() + timedelta(hours=hours)
        else:
            # Absolute time
            schedule_time = datetime.strptime(time, '%Y-%m-%d %H:%M')
    except ValueError:
        click.echo(f"{Fore.RED}✗ Invalid time format. Use 'YYYY-MM-DD HH:MM' or '30m' or '2h'{Style.RESET_ALL}")
        return
    
    # Check if time is in the future
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
    click.echo(f"\\n{Fore.YELLOW}⚠ Keep your computer running until the scheduled time{Style.RESET_ALL}")
    click.echo(f"Run '{Fore.CYAN}gitscheduler daemon{Style.RESET_ALL}' to start the scheduler")


@cli.command()
def list():
    \"\"\"List all scheduled commits\"\"\"
    gs = GitScheduler()
    
    if not gs.schedules:
        click.echo(f"{Fore.YELLOW}No scheduled commits{Style.RESET_ALL}")
        return
    
    click.echo(f"\\n{Fore.CYAN}{'='*80}{Style.RESET_ALL}")
    click.echo(f"{Fore.CYAN}Scheduled Commits{Style.RESET_ALL}")
    click.echo(f"{Fore.CYAN}{'='*80}{Style.RESET_ALL}\\n")
    
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


@cli.command()
@click.argument('schedule_id', type=int)
def cancel(schedule_id):
    \"\"\"Cancel a scheduled commit\"\"\"
    gs = GitScheduler()
    
    schedule = next((s for s in gs.schedules if s['id'] == schedule_id), None)
    
    if not schedule:
        click.echo(f"{Fore.RED}✗ Schedule #{schedule_id} not found{Style.RESET_ALL}")
        return
    
    if schedule['status'] != 'pending':
        click.echo(f"{Fore.RED}✗ Cannot cancel a {schedule['status']} schedule{Style.RESET_ALL}")
        return
    
    gs.remove_schedule(schedule_id)
    click.echo(f"{Fore.GREEN}✓ Cancelled schedule #{schedule_id}{Style.RESET_ALL}")


@cli.command()
def clear():
    \"\"\"Clear all completed/failed schedules\"\"\"
    gs = GitScheduler()
    original_count = len(gs.schedules)
    gs.schedules = [s for s in gs.schedules if s['status'] == 'pending']
    gs.save_schedules()
    removed = original_count - len(gs.schedules)
    click.echo(f"{Fore.GREEN}✓ Removed {removed} completed/failed schedules{Style.RESET_ALL}")


@cli.command()
def daemon():
    \"\"\"Run the scheduler daemon (keeps running to execute scheduled tasks)\"\"\"
    gs = GitScheduler()
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
    
    click.echo(f"{Fore.GREEN}✓ GitScheduler daemon started{Style.RESET_ALL}")
    click.echo(f"  Monitoring {pending_count} pending schedules")
    click.echo(f"  Log file: {LOG_FILE}")
    click.echo(f"\\n{Fore.YELLOW}Press Ctrl+C to stop{Style.RESET_ALL}\\n")
    
    # Handle graceful shutdown
    def signal_handler(sig, frame):
        click.echo(f"\\n{Fore.YELLOW}Shutting down scheduler...{Style.RESET_ALL}")
        gs.scheduler.shutdown()
        sys.exit(0)
    
    signal.signal(signal.SIGINT, signal_handler)
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        gs.scheduler.shutdown()


@cli.command()
def logs():
    \"\"\"View scheduler logs\"\"\"
    if LOG_FILE.exists():
        with open(LOG_FILE, 'r') as f:
            content = f.read()
            if content:
                click.echo(content)
            else:
                click.echo(f"{Fore.YELLOW}No logs yet{Style.RESET_ALL}")
    else:
        click.echo(f"{Fore.YELLOW}No logs yet{Style.RESET_ALL}")


if __name__ == '__main__':
    cli()
"""

print("✓ Created main CLI code")
print("✓ Created requirements.txt")
print("\nFiles ready to be generated!")
