import time
from threading import Thread
from winotify import Notification

class Alert:
    def __init__(self):
        self.last_behavior_alert_time = 0
        self.last_integrity_alert_time = 0
        self.alert_interval = 300  # 5분 (300초) 간격으로 알림 제한

    def _show_toast_async(self, toast):
        Thread(target=toast.show).start()

    def behavior_alert(self, eventid, username, description):
        current_time = time.time()
        if current_time - self.last_behavior_alert_time > self.alert_interval:
            toast = Notification(
                app_id="HIDS",
                title="Behavior Alert",
                msg=description,
                duration="short"
            )
            self._show_toast_async(toast)
            self.last_behavior_alert_time = current_time

    def integrity_alert(self, action, path, description):
        current_time = time.time()
        if current_time - self.last_integrity_alert_time > self.alert_interval:
            toast = Notification(
                app_id="HIDS",
                title="Integrity Alert",
                msg=description,
                duration="short"
            )
            self._show_toast_async(toast)
            self.last_integrity_alert_time = current_time
