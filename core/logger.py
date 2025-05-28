import os
import time
import threading
from datetime import datetime

class Logger:
    def __init__(self, config):
        self.config = config
        self.target_file = config.get('log_file_path', 'C:/logs/sample.log')
        self.output_file = config.get('output_log_file', 'logs/collected_logs.log')
        self.interval = config.get('collection_interval', 10)
        self.running = False
        self.thread = None
        self.last_position = 0
        
        # 출력 로그 디렉토리 자동 생성
        output_dir = os.path.dirname(self.output_file)
        if output_dir and not os.path.exists(output_dir):
            os.makedirs(output_dir, exist_ok=True)

    def current_time(self):
        return datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    def start(self):
        """로그 수집 백그라운드 시작"""
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
        """로그 파일에서 새로 추가된 라인 수집"""
        try:
            if not os.path.exists(self.target_file):
                print(f"[Logger] Target file not found: {self.target_file}")
                return

            with open(self.target_file, 'r', encoding='utf-8', errors='ignore') as f:
                f.seek(self.last_position)
                new_lines = f.readlines()
                self.last_position = f.tell()

                for line in new_lines:
                    self.write_log(line.strip())

        except Exception as e:
            print(f"[Logger] Error collecting logs: {e}")

    def write_log(self, message):
        """수집 로그를 output 파일에 기록"""
        try:
            timestamp = self.current_time()
            log_entry = f"{timestamp} - {message}"
            with open(self.output_file, 'a', encoding='utf-8') as f:
                f.write(log_entry + "\n")
        except Exception as e:
            print(f"[Logger] Error writing log: {e}")

    def stop(self):
        """로그 수집 중지"""
        self.running = False
        if self.thread:
            self.thread.join(timeout=2)
        print("[Logger] Stopped.")
