from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel, QProgressBar
from PyQt5.QtCore import Qt

# 시스템 모니터링 대시보드의 기본 위젯을 위한 클래스
class DashboardWidget(QWidget):
    def __init__(self, config, parent=None):
        super().__init__(parent)
        self.config = config

        # 레이아웃 설정
        self.layout = QVBoxLayout()

        # 시스템 모니터링 상태를 표시할 레이블
        self.status_label = QLabel("시스템 상태: 정상", self)
        self.layout.addWidget(self.status_label)

        # 파일 무결성 감시 진행 상태를 표시할 프로그레스 바
        self.progress_bar = QProgressBar(self)
        self.progress_bar.setRange(0, 100)  # 범위 설정 (0~100)
        self.layout.addWidget(self.progress_bar)

        # 경고 메시지를 띄울 버튼 (예시로 알림을 생성하는 버튼)
        self.alert_button = QPushButton("경고 메시지 보내기", self)
        self.alert_button.clicked.connect(self.show_alert)  # 버튼 클릭 시 경고 표시
        self.layout.addWidget(self.alert_button)

        # 레이아웃을 위젯에 설정
        self.setLayout(self.layout)

    # 경고 메시지 표시 함수 (예: 시스템 오류가 발생한 경우)
    def show_alert(self):
        self.status_label.setText("경고: 의심스러운 프로세스 발견!")
        self.progress_bar.setValue(50)  # 진행 상태 표시
        self.status_label.setStyleSheet("color: red; font-weight: bold;")  # 경고 메시지 스타일 설정


# 대시보드 전체를 구성하는 위젯 클래스
class Dashboard(QWidget):
    def __init__(self, config, parent=None):
        super().__init__(parent)
        self.config = config

        # 레이아웃 설정
        self.layout = QVBoxLayout()

        # 여러 개의 위젯 추가
        self.dashboard_widget = DashboardWidget(config, self)
        self.layout.addWidget(self.dashboard_widget)

        # 대시보드 전체 레이아웃을 위젯에 설정
        self.setLayout(self.layout)