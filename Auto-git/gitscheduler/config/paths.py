from pathlib import Path

CONFIG_DIR = Path.home() / ".gitscheduler"
SCHEDULE_FILE = CONFIG_DIR / "schedules.json"
LOG_FILE = CONFIG_DIR / "scheduler.log"
PID_FILE = CONFIG_DIR / "daemon.pid"

CONFIG_DIR.mkdir(exist_ok=True)
