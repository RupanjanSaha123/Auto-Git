from datetime import datetime, timedelta

def parse_time(time_str: str) -> datetime:
    if time_str.endswith("m"):
        return datetime.now() + timedelta(minutes=int(time_str[:-1]))
    if time_str.endswith("h"):
        return datetime.now() + timedelta(hours=int(time_str[:-1]))
    return datetime.strptime(time_str, "%Y-%m-%d %H:%M")
