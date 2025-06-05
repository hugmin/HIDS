import os
import json
from datetime import datetime
from typing import Dict, Any

from core.alert import Alert
from core.database import Database


class Detector:
    def __init__(self, db: Database, alert: Alert):
        self.db = db
        self.alert = alert
        self.log_directory = "C:/ProgramData/osquery/log"
        self.event_log_files = []

    def load_log_files(self) -> None:
        """로그 디렉토리에서 .log 파일 목록 수집"""
        for root, _, files in os.walk(self.log_directory):
            for file in files:
                if file.endswith(".log"):
                    self.event_log_files.append(os.path.join(root, file))

    def parse_event(self, log_entry: Dict[str, Any]) -> None:
        """단일 이벤트 파싱 및 DB 기록 + 알림 전송"""
        try:
            eventid = str(log_entry.get("columns", {}).get("eventid", "unknown"))
            action = log_entry.get("action", "unknown")
            username = log_entry.get("decorations", {}).get("username", "unknown")
            data_fields = log_entry.get("columns", {}).get("data", {})
            details = json.dumps(data_fields)

            alert_type = "Other"
            description = "Other event detected."

            if eventid == "4624":
                alert_type = "Behavior Detection"
                description = f"Successful login by {username}."
                # self.alert.behavior_alert(eventid, username, description) 알림 생략

            elif eventid == "4625":
                alert_type = "Behavior Detection"
                description = f"Failed login attempt by {username}."
                self.alert.behavior_alert(eventid, username, description)

            elif eventid == "4672":
                alert_type = "Behavior Detection"
                description = f"User {username} granted special privileges."
                self.alert.behavior_alert(eventid, username, description)

            elif eventid == "4688":
                alert_type = "Behavior Detection"
                process_name = data_fields.get("ProcessName", "Unknown")
                description = f"New process started: {process_name} by {username}."
                self.alert.behavior_alert(eventid, username, description)

            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            self.db.insert_event(alert_type, eventid, action, username, description, timestamp)

        except Exception as e:
            print(f"[Detector] Error parsing log entry: {e}")

    def process_logs(self) -> None:
        """모든 로그 파일 순회 및 이벤트 파싱"""
        for log_file in self.event_log_files:
            try:
                with open(log_file, 'r', encoding='utf-8') as file:
                    for line in file:
                        try:
                            log_entry = json.loads(line.strip())
                            self.parse_event(log_entry)
                        except json.JSONDecodeError:
                            print(f"[Detector] JSON decode error in file: {log_file}")
                        except Exception as e:
                            print(f"[Detector] Error in {log_file}: {e}")
            except FileNotFoundError:
                print(f"[Detector] File not found: {log_file}")
            except Exception as e:
                print(f"[Detector] Cannot open file {log_file}: {e}")

    def run(self) -> None:
        """탐지기 실행: 로그 로드 및 분석"""
        self.load_log_files()
        self.process_logs()
