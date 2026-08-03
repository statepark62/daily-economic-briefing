"""Gmail SMTP(앱 비밀번호)로 이메일을 발송하는 모듈."""

import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


def send_email(subject: str, body: str):
    sender = os.environ["MAIL_USERNAME"]
    password = os.environ["MAIL_PASSWORD"]
    recipient = os.environ["MAIL_TO"]

    msg = MIMEMultipart()
    msg["From"] = sender
    msg["To"] = recipient
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "plain", "utf-8"))

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(sender, password)
        server.sendmail(sender, recipient, msg.as_string())

    print(f"메일 발송 완료: {subject}")
