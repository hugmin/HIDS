import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from win10toast import ToastNotifier

class AlertManager:
    def __init__(self, logger, config):
        self.logger = logger
        self.config = config
        self.notifier = ToastNotifier()

        email_cfg = config.get("email", {})
        self.email_enabled = email_cfg.get("enabled", False)
        self.smtp_server = email_cfg.get("smtp_server")
        self.smtp_port = email_cfg.get("smtp_port")
        self.sender = email_cfg.get("sender")
        self.receiver = email_cfg.get("receiver")
        self.username = email_cfg.get("username")
        self.password = email_cfg.get("password")

    def send_alert(self, message):
        # 로컬 알림
        self.logger.write_log(message, level="CRITICAL", source="alert")
        self.notifier.show_toast("보안 경고", message, duration=5, threaded=True)

        # 이메일 알림
        if self.email_enabled:
            try:
                self._send_email(message)
                self.logger.write_log("이메일 알림 발송 성공", level="INFO", source="alert")
            except Exception as e:
                self.logger.write_log(f"이메일 알림 실패: {e}", level="ERROR", source="alert")

    def _send_email(self, message):
        msg = MIMEMultipart()
        msg['From'] = self.sender
        msg['To'] = self.receiver
        msg['Subject'] = "보안 경고 알림"

        body = MIMEText(message, 'plain')
        msg.attach(body)

        with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
            server.starttls()
            server.login(self.username, self.password)
            server.send_message(msg)
