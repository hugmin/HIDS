import os
import time
import threading
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from utils.hashing import calculate_sha256

class IntegrityMonitor:
    def __init__(self, config, logger, db, alert):
        self.config = config
        self.logger = logger
        self.db = db
        self.alert = alert
        self.directories = config.get("monitor_directories", [])
        self.interval = config.get("integrity_check_interval", 3600)
        self.observers = []

    def start(self):
        self.logger.write_log("Starting integrity monitor...", source="integrity_monitor")
        self._start_realtime_monitoring()
        threading.Thread(target=self._start_periodic_check, daemon=True).start()

    def _start_realtime_monitoring(self):
        for directory in self.directories:
            if not os.path.exists(directory):
                self.logger.write_log(f"Directory not found: {directory}", level="WARNING", source="integrity_monitor")
                continue

            event_handler = FileChangeHandler(self.logger, self.db, self.alert)
            observer = Observer()
            observer.schedule(event_handler, directory, recursive=True)
            observer.start()
            self.observers.append(observer)
            self.logger.write_log(f"Watching directory: {directory}", source="integrity_monitor")

    def _start_periodic_check(self):
        while True:
            self.logger.write_log("Performing periodic integrity check...", source="integrity_monitor")
            for directory in self.directories:
                self._check_directory_integrity(directory)
            time.sleep(self.interval)

    def _check_directory_integrity(self, directory):
        for root, _, files in os.walk(directory):
            for file in files:
                filepath = os.path.join(root, file)
                if not os.path.isfile(filepath):
                    continue
                current_hash = calculate_sha256(filepath)
                stored_hash = self.db.get_hash_for_file(filepath)

                if stored_hash and current_hash != stored_hash:
                    msg = f"File tampering detected: {filepath}"
                    self.logger.write_log(msg, level="WARNING", source="integrity_monitor")
                    self.alert.send_alert(msg)

                # 최신 해시값으로 DB 업데이트
                self.db.insert_or_update_file_hash(filepath, current_hash)

    def stop(self):
        for observer in self.observers:
            observer.stop()
            observer.join()
        self.logger.write_log("Stopped integrity monitor.", source="integrity_monitor")


class FileChangeHandler(FileSystemEventHandler):
    def __init__(self, logger, db, alert):
        super().__init__()
        self.logger = logger
        self.db = db
        self.alert = alert

    def on_modified(self, event):
        self._handle_event(event, "MODIFIED")

    def on_created(self, event):
        self._handle_event(event, "CREATED")

    def _handle_event(self, event, event_type):
        if event.is_directory:
            return
        filepath = event.src_path
        hash_value = calculate_sha256(filepath)
        stored_hash = self.db.get_hash_for_file(filepath)

        if stored_hash and hash_value != stored_hash:
            msg = f"File {event_type}: Tampering suspected at {filepath}"
            self.logger.write_log(msg, level="WARNING", source="integrity_monitor")
            self.alert.send_alert(msg)

        self.db.insert_or_update_file_hash(filepath, hash_value)
