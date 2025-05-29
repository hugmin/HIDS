from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel
from PyQt5.QtCore import QTimer
from core.system_monitor import SystemMonitor

class SystemMonitorWidget(QWidget):
    def __init__(self):
        print("[SystemMonitorWidget] 생성자 진입")
        super().__init__()
        try:
            self.monitor = SystemMonitor()
            print("[SystemMonitorWidget] SystemMonitor 생성 완료")
        except Exception as e:
            print(f"[SystemMonitorWidget] ❌ SystemMonitor 생성 실패: {e}")
            import traceback
            traceback.print_exc()
            raise

        self.init_ui()
        self.start_timer()

    def init_ui(self):
        layout = QVBoxLayout()

        self.cpu_label = QLabel()
        self.mem_label = QLabel()
        self.disk_label = QLabel()

        label_style = "font-size: 14px; padding: 2px;"
        self.cpu_label.setStyleSheet(label_style)
        self.mem_label.setStyleSheet(label_style)
        self.disk_label.setStyleSheet(label_style)

        layout.addWidget(self.cpu_label)
        layout.addWidget(self.mem_label)
        layout.addWidget(self.disk_label)

        self.setLayout(layout)
        self.update_stats()

    def start_timer(self):
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_stats)
        self.timer.start(3000)

    def update_stats(self):
        stats = self.monitor.get_stats()
        self.cpu_label.setText(f"🖥️ CPU 사용률: {stats['cpu']:.1f}%")
        self.mem_label.setText(f"🧠 메모리 사용률: {stats['memory']:.1f}%")
        self.disk_label.setText(f"💽 디스크 사용량: {stats['disk']:.1f}%")
