import json
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import os

WATCH_DIR = "/home/ubuntu/bsm/test"
LOG_FILE = "/home/ubuntu/bsm/logs/changes.json"

class ChangeHandler(FileSystemEventHandler):
    def on_modified(self, event):
        self.log_event("Modified", event)

    def on_created(self, event):
        self.log_event("Created", event)

    def on_deleted(self, event):
        self.log_event("Deleted", event)

    def log_event(self, action, event):
        if not event.is_directory:
            log_data = {
                "action": action,
                "file": event.src_path,
                "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
            }
            with open(LOG_FILE, "a") as log_file:
                json.dump(log_data, log_file)
                log_file.write("\n")
            print(f"Logged: {log_data}")

if __name__ == "__main__":
    print(f"Monitoring {WATCH_DIR} for changes...")
    event_handler = ChangeHandler()
    observer = Observer()
    observer.schedule(event_handler, WATCH_DIR, recursive=True)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
