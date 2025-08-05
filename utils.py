import json
import os
from datetime import datetime

DATA_FILE = "data.json"

def load_data():
    if not os.path.exists(DATA_FILE):
        return {
            "websites": [],
            "visited_today": [],
            "last_reset": "",
            "reset_time": "00:00"
        }
    with open(DATA_FILE, "r") as f:
        return json.load(f)

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)

def reset_if_needed(data):
    today = datetime.now().strftime("%Y-%m-%d")
    if data.get("last_reset") != today:
        data["visited_today"] = []
        data["last_reset"] = today
        save_data(data)

def is_within_alarm_range(reset_time_str, hours_before=2):
    now = datetime.now()
    reset_time = datetime.strptime(reset_time_str, "%H:%M").replace(
        year=now.year, month=now.month, day=now.day
    )
    delta = reset_time - now
    return 0 < delta.total_seconds() <= hours_before * 3600
