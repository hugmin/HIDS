import sys
import os
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QLabel,
    QTextEdit, QPushButton
)
from PyQt5.QtCore import QTimer
from gui.widgets import SystemMonitorWidget

class Dashboard(QMainWindow):
    def __init__(self, config, logger):
        super().__init__()
        self.setWindowTitle("보안 모니터링 대시보드")
        self.setGeometry(200, 200, 900, 600)

        self.config = config
        self.logger = logger
        self.log_file = config.get("output_log_file", "logs/collected_logs.log")

        self.init_ui()
        self.update_logs()

        # 실시간 로그 리프레시 타이머
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_logs)
        self.timer.start(5000)  # 5초마다 갱신

    def init_ui(self):
        central_widget = QWidget()
        layout = QVBoxLayout()

        # 제목
        title = QLabel("📊 보안 모니터링 대시보드")
        title.setStyleSheet("font-size: 20px; font-weight: bold; margin-bottom: 10px;")
        layout.addWidget(title)

        # 시스템 리소스 모니터링 위젯 추가
        self.sys_monitor = SystemMonitorWidget()
        layout.addWidget(self.sys_monitor)

        # 로그 보기 영역
        self.log_view = QTextEdit()
        self.log_view.setReadOnly(True)
        layout.addWidget(self.log_view)

        # 새로고침 버튼
        refresh_btn = QPushButton("새로고침")
        refresh_btn.clicked.connect(self.update_logs)
        layout.addWidget(refresh_btn)

        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

    def update_logs(self):
        try:
            if os.path.exists(self.log_file):
                with open(self.log_file, 'r', encoding='utf-8') as f:
                    logs = f.read()
                self.log_view.setPlainText(logs)
            else:
                self.log_view.setPlainText("⚠️ 로그 파일이 존재하지 않습니다.")
        except Exception as e:
            error_msg = f"로그 갱신 중 오류: {e}"
            self.logger.write_log(error_msg, level="ERROR", source="dashboard")
            self.log_view.setPlainText(error_msg)
