import json
from config.paths import SCHEDULE_FILE

def load_schedules():
    if SCHEDULE_FILE.exists():
        try:
            return json.loads(SCHEDULE_FILE.read_text())
        except:
            return []
    return []

def save_schedules(data):
    SCHEDULE_FILE.write_text(json.dumps(data, indent=2))
