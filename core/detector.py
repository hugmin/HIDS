import wmi
import os
import time
from utils.hashing import calculate_sha256
from utils.rules import load_malicious_hashes

FAILED_LOGON_EVENT_ID = "4625"
MAX_FAILED_ATTEMPTS = 3
FAILED_ATTEMPT_WINDOW = 60  # seconds

class Detector:
    def __init__(self, config, logger, db, alert):
        self.config = config
        self.logger = logger
        self.db = db
        self.alert = alert
        self.failed_logins = {}  # {user: [timestamp1, timestamp2, ...]}
        self.malicious_hashes = set(config.get("malicious_hashes", []))

        self.wmi_conn = wmi.WMI()

    def start(self):
        self.logger.write_log("Starting detector module...", source="detector")
        while True:
            self.detect_failed_logins()
            self.detect_malware_execution()
            time.sleep(5)

    def detect_failed_logins(self):
        try:
            query = f"SELECT * FROM Win32_NTLogEvent WHERE Logfile='Security' AND EventCode={FAILED_LOGON_EVENT_ID}"
            for event in self.wmi_conn.query(query):
                user = event.InsertionStrings[5] if len(event.InsertionStrings) > 5 else "Unknown"
                self.track_failed_attempt(user)
        except Exception as e:
            self.logger.write_log(f"Failed to query login events: {e}", level="ERROR", source="detector")

    def track_failed_attempt(self, user):
        now = time.time()
        if user not in self.failed_logins:
            self.failed_logins[user] = []
        self.failed_logins[user] = [t for t in self.failed_logins[user] if now - t < FAILED_ATTEMPT_WINDOW]
        self.failed_logins[user].append(now)

        if len(self.failed_logins[user]) >= MAX_FAILED_ATTEMPTS:
            msg = f"Brute-force login suspected for user '{user}'"
            self.logger.write_log(msg, level="WARNING", source="detector")
            self.alert.send_alert(msg)
            self.failed_logins[user] = []  # reset after alert

    def detect_malware_execution(self):
        try:
            for process in self.wmi_conn.Win32_Process():
                path = process.ExecutablePath
                if not path or not os.path.isfile(path):
                    continue
                hash_val = calculate_sha256(path)
                if hash_val in self.malicious_hashes:
                    msg = f"Malware execution detected: {path}"
                    self.logger.write_log(msg, level="CRITICAL", source="detector")
                    self.alert.send_alert(msg)
        except Exception as e:
            self.logger.write_log(f"Failed malware detection: {e}", level="ERROR", source="detector")
