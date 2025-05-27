import time
import os
from utils.common import current_time

class Logger:
    def __init__(self, config):
        self.config = config
        self.log_file = self.config.get('log_file', 'system_logs.txt')

    def start(self):
        # 로그 수집 시작
        while True:
            self.collect_logs()
            time.sleep(10)

    def collect_logs(self):
        # 시스템 로그 수집
        timestamp = current_time('%Y-%m-%d %H:%M:%S')
        log_message = f"{timestamp} - Log collected"
        self.write_log(log_message)

    def write_log(self, log_message):
        # 로그 파일에 기록
        with open(self.log_file, 'a') as f:
            f.write(log_message + "\n")

    def stop(self):
        # 로그 수집 종료
        print("Logger stopped.")