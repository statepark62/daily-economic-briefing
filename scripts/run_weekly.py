import os
from datetime import datetime

from fetch_data import collect_all
from analyze import generate_weekly_report
from send_email import send_email

def main():
    data = collect_all()
    report = generate_weekly_report(data)

    today = datetime.utcnow().strftime("%Y-%m-%d")
    subject = f"[주간 경제 브리핑] {today}"
    send_email(subject, report)

    # 아카이브 저장 (repo/reports/weekly/에 커밋되도록 워크플로우에서 처리)
    os.makedirs("reports/weekly", exist_ok=True)
    with open(f"reports/weekly/{today}.md", "w", encoding="utf-8") as f:
        f.write(f"# 주간 경제 브리핑 ({today})\n\n{report}\n")


if __name__ == "__main__":
    main()
