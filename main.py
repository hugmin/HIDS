import sys
import json
from PyQt5.QtWidgets import QApplication, QMainWindow
from gui.dashboard import Dashboard
from core.logger import Logger
from core.integrity_monitor import IntegrityMonitor
from core.alert import AlertSystem
from core.detector import AnomalyDetector
from core.system_monitor import SystemMonitor
from core.database import Database

class HIDS(QMainWindow):
    def __init__(self):
        super().__init__()

        # 윈도우 설정
        self.setWindowTitle("HIDS - Host Intrusion Detection System")
        self.setGeometry(100, 100, 800, 600)

        # 설정 파일 로드
        self.load_config()

        # 대시보드 설정
        self.setup_dashboard()

        # 모니터링 시작
        self.start_monitoring()

    def load_config(self):
        # 설정 파일을 로드하는 메서드
        with open('config.json', 'r') as file:
            self.config = json.load(file)

    def setup_dashboard(self):
        # 대시보드 위젯을 설정하는 메서드
        self.dashboard = Dashboard(self.config)
        self.setCentralWidget(self.dashboard)

    def start_monitoring(self):
        # 시스템 모니터링 시작 메서드
        self.logger = Logger(self.config)
        self.integrity_monitor = IntegrityMonitor(self.config)
        self.alert_system = AlertSystem(self.config)
        self.detector = AnomalyDetector(self.config)
        self.system_monitor = SystemMonitor(self.config)
        self.database = Database(self.config)

        # 각 모듈 시작
        self.integrity_monitor.start()
        self.system_monitor.start()

    def closeEvent(self, event):
        # 창을 닫을 때 모니터링 종료
        self.integrity_monitor.stop()
        self.system_monitor.stop()
        self.logger.stop()
        event.accept()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = HIDS()
    window.show()
    sys.exit(app.exec_())
