import sys
import threading
import time
import subprocess
from PyQt5.QtWidgets import QApplication

from core.detector import Detector
from core.integrity_monitor import IntegrityMonitor
from core.alert import Alert
from core.database import Database
from gui.dashboard import Dashboard
from deploy.osquery_install import install_osquery, generate_osquery_config, ensure_log_dir

LOG_DIR = "C:/ProgramData/osquery/log"

def run_background_services():
    """osquery 설치, 로그 디렉토리 설정, 탐지기/모니터 실행"""
    install_osquery()
    generate_osquery_config()
    ensure_log_dir()

    db = Database()
    alert = Alert()
    detector = Detector(db, alert)
    integrity_monitor = IntegrityMonitor(db, alert)
    integrity_monitor.run()

    # 지속적으로 로그 감시 (polling 방식, watchdog 생략 가능)
    while True:
        detector.run()
        time.sleep(10)  # 10초마다 새로운 로그 감지 및 처리

def start_osquery_daemon():
    """osqueryd 실행 (이미 설치된 경우만)"""
    OSQUERY_EXE = "C:/Program Files/osquery/osqueryd/osqueryd.exe"
    OSQUERY_CONF = "C:/ProgramData/osquery/osquery.conf"

    try:
        subprocess.Popen([
            OSQUERY_EXE,
            f"--flagfile={OSQUERY_CONF}"
        ], creationflags=subprocess.CREATE_NO_WINDOW)
        print("osqueryd started.")
    except Exception as e:
        print(f"Failed to start osqueryd: {e}")

def main():
    # 백그라운드 스레드에서 osquery 실행 + 감시기 구동
    threading.Thread(target=start_osquery_daemon, daemon=True).start()
    threading.Thread(target=run_background_services, daemon=True).start()

    # GUI 실행
    app = QApplication(sys.argv)
    window = Dashboard()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
