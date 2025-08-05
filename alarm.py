import threading
import time
from utils import load_data, reset_if_needed, is_within_alarm_range
from plyer import notification
from playsound import playsound
import os

ALARM_SOUND = "alarm.mp3"  # Make sure this file exists

def alarm_loop():
    while True:
        data = load_data()
        reset_if_needed(data)

        total = len(data["websites"])
        visited = len(data["visited_today"])

        if total > 0 and visited < total:
            if is_within_alarm_range(data["reset_time"]):
                # Send desktop notification
                notification.notify(
                    title="DoTask Reminder",
                    message=f"You visited {visited}/{total} sites today!",
                    timeout=10
                )

                # Play alarm sound (once)
                if os.path.exists(ALARM_SOUND):
                    playsound(ALARM_SOUND)

                time.sleep(3600)  # wait 1 hour before next alarm
            else:
                time.sleep(300)  # check every 5 minutes
        else:
            time.sleep(300)

def start_alarm():
    threading.Thread(target=alarm_loop, daemon=True).start()
