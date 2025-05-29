import os
import time
import threading
from datetime import datetime

class Logger:
    def __init__(self, config, db=None):
        self.config = config
        self.db = db
        self.target_file = config.get('log_file_path', 'C:/logs/sample.log')
        self.output_file = config.get('output_log_file', 'C:/logs/collected_logs.log')
        self.interval = config.get('collection_interval', 10)
        self.running = False
        self.thread = None
        self.last_position = 0

        # output_file 폴더가 없으면 자동 생성
        output_dir = os.path.dirname(self.output_file)
        if output_dir and not os.path.exists(output_dir):
            os.makedirs(output_dir, exist_ok=True)

        # target_file 폴더도 생성 (선택사항인데 혹시 몰라서)
        target_dir = os.path.dirname(self.target_file)
        if target_dir and not os.path.exists(target_dir):
            os.makedirs(target_dir, exist_ok=True)

    def current_time(self):
        return datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    def start(self):
        if not self.running:
            self.running = True
            self.thread = threading.Thread(target=self._run, daemon=True)
            self.thread.start()
            print(f"[Logger] Started monitoring: {self.target_file}")

    def _run(self):
        while self.running:
            self.collect_logs()
            time.sleep(self.interval)

    def collect_logs(self):
        if not os.path.exists(self.target_file):
            return
        with open(self.target_file, 'r', encoding='utf-8', errors='ignore') as f:
            f.seek(self.last_position)
            new_lines = f.readlines()
            self.last_position = f.tell()
            for line in new_lines:
                self.write_log(line.strip(), source="logfile")

    def write_log(self, message, level="INFO", source="system"):
        timestamp = self.current_time()
        entry = f"{timestamp} [{level}] ({source}) {message}"
        try:
            with open(self.output_file, 'a', encoding='utf-8') as f:
                f.write(entry + "\n")
            if self.db:
                self.db.insert_log({
                    "timestamp": timestamp,
                    "level": level,
                    "source": source,
                    "message": message
                })
        except Exception as e:
            print(f"[Logger] Write error: {e}")

    def stop(self):
        self.running = False
        if self.thread:
            self.thread.join(timeout=2)
        print("[Logger] Stopped.")
