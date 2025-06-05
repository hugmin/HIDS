import psutil
from PyQt5.QtCore import QObject, pyqtSignal

class SystemMonitor(QObject):
    system_info_updated = pyqtSignal(float, float, float)

    def __init__(self):
        super().__init__()
        self.cpu_usage = 0
        self.memory_usage = 0
        self.disk_usage = 0

    def collect_and_emit_system_info(self):
        self.cpu_usage = psutil.cpu_percent()
        self.memory_usage = psutil.virtual_memory().percent
        self.disk_usage = psutil.disk_usage('/').percent
        self.system_info_updated.emit(self.cpu_usage, self.memory_usage, self.disk_usage)
