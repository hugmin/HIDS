import sys
import json
import threading
from PyQt5.QtWidgets import QApplication

from core.logger import Logger
from core.detector import Detector
from core.database import DatabaseManager
from core.integrity_monitor import IntegrityMonitor
from core.alert import AlertManager
from gui.dashboard import Dashboard

def load_config():
    try:
        print("[main.py] config.json 로딩 시작")
        with open("config.json", "r", encoding="utf-8") as f:
            config = json.load(f)
        print("[main.py] config.json 로딩 성공")
        return config
    except Exception as e:
        print(f"[main.py] config.json 로딩 실패: {e}")
        sys.exit(1)

def main():
    print("[main.py] main 시작")

    config = load_config()
    print("[main.py] 설정 로드 완료")

    try:
        print("[main.py] DB 초기화 시작")
        db = DatabaseManager(config["database"])
        print("[main.py] DB 초기화 완료")
    except Exception as e:
        print(f"[main.py] ❌ DB 초기화 실패: {e}")
        sys.exit(1)

    print("[main.py] Logger 초기화 시작")
    logger = Logger(config, db)
    print("[main.py] Logger 초기화 완료")

    print("[main.py] AlertManager 초기화 시작")
    alert = AlertManager(logger, config)
    print("[main.py] AlertManager 초기화 완료")

    print("[main.py] Detector 초기화 시작")
    detector = Detector(config, logger, db, alert)
    print("[main.py] Detector 초기화 완료")

    print("[main.py] IntegrityMonitor 초기화 시작")
    integrity_monitor = IntegrityMonitor(config, logger, db, alert)
    print("[main.py] IntegrityMonitor 초기화 완료")

    logger.start()
    print("[main.py] Logger started")

    threading.Thread(target=detector.start, daemon=True).start()
    threading.Thread(target=integrity_monitor.start, daemon=True).start()

    try:
        app = QApplication(sys.argv)
        dashboard = Dashboard(config, logger)
        dashboard.show()
        print("[main.py] 대시보드 실행 완료")
        sys.exit(app.exec_())
    except Exception as e:
        import traceback
        print(f"[main.py] GUI 실행 중 예외 발생: {e}")
        traceback.print_exc()

if __name__ == "__main__":
    print("[main.py] main 시작")
    try:
        main()
    except Exception as e:
        import traceback
        print("[main.py] 예외 발생:")
        traceback.print_exc()
