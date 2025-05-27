from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout

class Dashboard(QWidget):
    def __init__(self, config):
        super().__init__()
        self.config = config
        self.init_ui()

    def init_ui(self):
        # UI 설정
        self.setWindowTitle('HIDS Dashboard')
        layout = QVBoxLayout()

        self.label = QLabel("System Status: Monitoring...")
        layout.addWidget(self.label)

        self.setLayout(layout)