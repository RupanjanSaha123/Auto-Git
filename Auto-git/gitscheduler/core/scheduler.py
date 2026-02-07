from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.date import DateTrigger

from core.storage import load_schedules, save_schedules
from core.git_ops import execute_git
from utils.logger import log

class GitScheduler:
    def __init__(self):
        self.schedules = load_schedules()
        self.scheduler = BackgroundScheduler()

    def add(self, repo, message, branch, run_time):
        sid = len(self.schedules) + 1
        self.schedules.append({
            "id": sid,
            "repo": str(repo),
            "message": message,
            "branch": branch,
            "time": run_time.isoformat(),
            "status": "pending"
        })
        save_schedules(self.schedules)
        return sid

    def execute(self, sid):
        schedule = next(s for s in self.schedules if s["id"] == sid)
        try:
            result = execute_git(
                schedule["repo"],
                schedule["message"],
                schedule["branch"]
            )
            schedule["status"] = result
            log(f"{result.upper()} → {schedule['message']}")
        except Exception as e:
            schedule["status"] = "failed"
            schedule["error"] = str(e)
            log(f"FAILED → {e}")

        save_schedules(self.schedules)

    def load_jobs(self):
        for s in self.schedules:
            if s["status"] == "pending":
                run_time = datetime.fromisoformat(s["time"])
                if run_time > datetime.now():
                    self.scheduler.add_job(
                        self.execute,
                        DateTrigger(run_date=run_time),
                        args=[s["id"]]
                    )
