import time
import psutil

class SystemMonitor:
    def __init__(self, config):
        self.config = config

    def start(self):
        # 시스템 모니터링 시작
        while True:
            self.monitor_system()
            time.sleep(10)

    def monitor_system(self):
        # 시스템 상태를 모니터링
        for proc in psutil.process_iter(['pid', 'name']):
            if proc.info['name'] == 'suspicious_program.exe':  # 의심스러운 프로세스 감지
                print(f"Suspicious process detected: {proc.info['pid']}")
                self.send_alert(f"Suspicious process detected: {proc.info['name']}")

    def send_alert(self, message):
        # 알림 전송
        print(f"Alert: {message}")

    def stop(self):
        # 시스템 모니터링 종료
        print("System Monitor stopped.")