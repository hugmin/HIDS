import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

class AlertSystem:
    def __init__(self, config):
        self.config = config

    def send_email(self, subject, body):
        # 이메일 알림 전송
        sender_email = self.config['email']['sender']
        receiver_email = self.config['email']['receiver']
        password = self.config['email']['password']

        message = MIMEMultipart()
        message['From'] = sender_email
        message['To'] = receiver_email
        message['Subject'] = subject
        message.attach(MIMEText(body, 'plain'))

        with smtplib.SMTP_SSL(self.config['email']['smtp_server'], self.config['email']['smtp_port']) as server:
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_email, message.as_string())

    def send_toast(self, message):
        # 토스트 알림 전송
        print(f"Toast: {message}")

    def send_alert(self, message):
        # 알림 시스템으로 경고 전송
        self.send_email("Alert", message)
        self.send_toast(message)