import os
import hashlib
import json
import threading
from datetime import datetime
from typing import List, Dict, Any

from PyQt5.QtCore import QTimer
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

from core.alert import Alert
from core.database import Database


class IntegrityMonitor(FileSystemEventHandler):
    def __init__(self, db: Database, alert: Alert):
        self.db = db
        self.alert = alert
        self.monitor_path = f"C:/Users/{os.getlogin()}/OneDrive/문서"
        self.event_queue: List[Dict[str, Any]] = []
        self.lock = threading.Lock()

        # 이벤트 병합 및 처리 타이머
        self.timer = QTimer()
        self.timer.timeout.connect(self.process_buffered_events)
        self.timer.start(5000)  # 5초마다 병합 및 처리

        # watchdog 설정
        self.observer = Observer()
        self.observer.schedule(self, self.monitor_path, recursive=True)

    def run(self):
        """모니터 시작"""
        print(f"[IntegrityMonitor] Starting to monitor: {self.monitor_path}")
        self.observer.start()

    def stop(self):
        """모니터 종료"""
        self.observer.stop()
        self.observer.join()

    def on_created(self, event):
        if not event.is_directory:
            self.queue_event("added", event.src_path)

    def on_deleted(self, event):
        if not event.is_directory:
            self.queue_event("removed", event.src_path)

    def on_modified(self, event):
        if not event.is_directory:
            self.queue_event("modified", event.src_path)

    def queue_event(self, action: str, path: str):
        with self.lock:
            self.event_queue.append({
                "timestamp": datetime.now(),
                "action": action,
                "path": path,
                "md5": self.calculate_md5(path) if action != "removed" else ""
            })

    def process_buffered_events(self):
        with self.lock:
            if not self.event_queue:
                return

            events = self.event_queue.copy()
            self.event_queue.clear()

        merged = self.merge_modified_events(events)

        for event in merged:
            self.save_event_and_alert(event)

    def merge_modified_events(self, events: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """CREATED+DELETED 조합을 MODIFIED로 간주하는 로직"""
        events.sort(key=lambda x: (x["path"], x["timestamp"]))
        result = []
        i = 0

        while i < len(events):
            cur = events[i]

            if i + 1 < len(events):
                nxt = events[i + 1]
                if (
                    cur["path"] == nxt["path"]
                    and cur["action"] == "removed"
                    and nxt["action"] == "added"
                    and cur["md5"] != nxt["md5"]
                ):
                    result.append({
                        "timestamp": nxt["timestamp"],
                        "action": "MODIFIED",
                        "path": nxt["path"]
                    })
                    i += 2
                    continue

            action_map = {"added": "CREATED", "removed": "DELETED"}
            mapped_action = action_map.get(cur["action"], cur["action"].upper())
            result.append({
                "timestamp": cur["timestamp"],
                "action": mapped_action,
                "path": cur["path"]
            })
            i += 1

        return sorted(result, key=lambda x: x["timestamp"])

    def save_event_and_alert(self, event: Dict[str, Any]) -> None:
        try:
            action = event["action"]
            path = event["path"]
            timestamp = event["timestamp"].strftime('%Y-%m-%d %H:%M:%S')
            username = "SYSTEM@NT AUTHORITY"

            # 알림 전송
            self.alert.integrity_alert(action, path, f"File {path} was {action.lower()}.")

            # DB 저장
            alert_type = "Integrity Check"
            description = f"File {path} was {action.lower()} by {username}"
            self.db.insert_event(alert_type, "Integrity Event", action, username, description, timestamp)

        except Exception as e:
            print(f"[IntegrityMonitor] Error saving alert: {e}")

    def calculate_md5(self, filepath: str) -> str:
        try:
            with open(filepath, 'rb') as f:
                return hashlib.md5(f.read()).hexdigest()
        except Exception:
            return ""
