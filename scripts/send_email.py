"""Gmail SMTP(앱 비밀번호)로 이메일을 발송하는 모듈. plain / HTML 겸용."""

import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


def send_email(subject: str, plain_body: str, html_body: str = None):
    sender = os.environ["MAIL_USERNAME"]
    password = os.environ["MAIL_PASSWORD"]
    recipient = os.environ["MAIL_TO"]

    msg = MIMEMultipart("alternative")
    msg["From"] = sender
    msg["To"] = recipient
    msg["Subject"] = subject

    # 플레인 텍스트를 먼저 붙이고, HTML을 나중에 붙여야
    # 대부분의 메일 클라이언트가 HTML 버전을 우선 렌더링합니다.
    msg.attach(MIMEText(plain_body, "plain", "utf-8"))
    if html_body:
        msg.attach(MIMEText(html_body, "html", "utf-8"))

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(sender, password)
        server.sendmail(sender, recipient, msg.as_string())

    print(f"메일 발송 완료: {subject}")
