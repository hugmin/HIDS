import sys
import sqlite3
import datetime
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QTabWidget, QLabel
from PyQt5.QtCore import QTimer, pyqtSignal, QObject
import psutil
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

class SystemMonitor(QObject):
    system_info_updated = pyqtSignal(float, float, float)

    def __init__(self):
        super().__init__()

    def monitor_system(self):
        cpu_usage = psutil.cpu_percent()
        memory_usage = psutil.virtual_memory().percent
        disk_usage = psutil.disk_usage('/').percent
        self.system_info_updated.emit(cpu_usage, memory_usage, disk_usage)

def fetch_behavior_data():
    try:
        conn = sqlite3.connect('events.db')
        cursor = conn.cursor()
        query = '''
        SELECT strftime('%Y-%m-%d', timestamp) AS date, COUNT(*) AS event_count
        FROM events
        WHERE alert_type = 'behavior'
          AND timestamp >= datetime('now', '-7 days')
        GROUP BY date
        ORDER BY date;
        '''
        cursor.execute(query)
        rows = cursor.fetchall()
        conn.close()
        return rows
    except Exception as e:
        print(f"Error fetching behavior data: {e}")
        return []

def fetch_integrity_data():
    try:
        conn = sqlite3.connect('events.db')
        cursor = conn.cursor()
        query = '''
        SELECT strftime('%Y-%m-%d', timestamp) AS date, COUNT(*) AS event_count
        FROM events
        WHERE alert_type = 'integrity'
          AND timestamp >= datetime('now', '-7 days')
        GROUP BY date
        ORDER BY date;
        '''
        cursor.execute(query)
        rows = cursor.fetchall()
        conn.close()
        return rows
    except Exception as e:
        print(f"Error fetching integrity data: {e}")
        return []

class Dashboard(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('HIDS Dashboard')
        self.resize(1000, 700)

        self.system_monitor = SystemMonitor()
        self.system_monitor.system_info_updated.connect(self.update_system_info)

        layout = QVBoxLayout()

        self.cpu_label = QLabel('CPU Usage: 0%')
        self.memory_label = QLabel('Memory Usage: 0%')
        self.disk_label = QLabel('Disk Usage: 0%')

        layout.addWidget(self.cpu_label)
        layout.addWidget(self.memory_label)
        layout.addWidget(self.disk_label)

        self.tab_widget = QTabWidget()

        self.behavior_tab = QWidget()
        self.behavior_layout = QVBoxLayout()
        self.behavior_tab.setLayout(self.behavior_layout)

        self.integrity_tab = QWidget()
        self.integrity_layout = QVBoxLayout()
        self.integrity_tab.setLayout(self.integrity_layout)

        self.tab_widget.addTab(self.behavior_tab, "Behavior Detection")
        self.tab_widget.addTab(self.integrity_tab, "Integrity Check")

        layout.addWidget(self.tab_widget)

        self.setLayout(layout)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.system_monitor.monitor_system)
        self.timer.start(1000)

        self.update_graphs()

    def update_system_info(self, cpu_usage, memory_usage, disk_usage):
        self.cpu_label.setText(f'CPU Usage: {cpu_usage}%')
        self.memory_label.setText(f'Memory Usage: {memory_usage}%')
        self.disk_label.setText(f'Disk Usage: {disk_usage}%')

    def update_graphs(self):
        behavior_data = fetch_behavior_data()
        integrity_data = fetch_integrity_data()

        # 데이터가 없더라도 그래프를 그리도록 빈 리스트라도 넘겨 처리
        self.update_behavior_graph(behavior_data if behavior_data else [])
        self.update_integrity_graph(integrity_data if integrity_data else [])

    def clear_layout(self, layout):
        for i in reversed(range(layout.count())):
            widget = layout.itemAt(i).widget()
            if widget is not None:
                widget.deleteLater()

    def update_behavior_graph(self, behavior_data):
        self.clear_layout(self.behavior_layout)

        today = datetime.date.today()
        last_7_days = [(today - datetime.timedelta(days=i)).strftime('%Y-%m-%d') for i in reversed(range(7))]
        data_dict = dict(behavior_data)
        event_counts = [data_dict.get(date, 0) for date in last_7_days]

        fig, ax = plt.subplots(figsize=(5, 3))
        ax.bar(last_7_days, event_counts)
        ax.set_title("Behavior Detection (Last 7 Days)")
        ax.set_xlabel("Date")
        ax.set_ylabel("Event Count")
        # x축 라벨 회전 제거 (기본 0도)
        ax.tick_params(axis='x', rotation=0)

        canvas = FigureCanvas(fig)
        self.behavior_layout.addWidget(canvas)

    def update_integrity_graph(self, integrity_data):
        self.clear_layout(self.integrity_layout)

        today = datetime.date.today()
        last_7_days = [(today - datetime.timedelta(days=i)).strftime('%Y-%m-%d') for i in reversed(range(7))]
        data_dict = dict(integrity_data)
        event_counts = [data_dict.get(date, 0) for date in last_7_days]

        fig, ax = plt.subplots(figsize=(5, 3))
        ax.bar(last_7_days, event_counts)
        ax.set_title("File Integrity Check (Last 7 Days)")
        ax.set_xlabel("Date")
        ax.set_ylabel("Event Count")
        # x축 라벨 회전 제거
        ax.tick_params(axis='x', rotation=0)

        canvas = FigureCanvas(fig)
        self.integrity_layout.addWidget(canvas)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Dashboard()
    window.show()
    sys.exit(app.exec_())
