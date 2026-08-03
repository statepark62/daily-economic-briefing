import os
from datetime import datetime

from fetch_data import collect_all
from analyze import generate_weekly_report
from send_email import send_email
from html_template import render_report_html


def main():
    data = collect_all()
    report_md = generate_weekly_report(data)

    today = datetime.utcnow().strftime("%Y-%m-%d")
    subject = f"[주간 경제 브리핑] {today}"

    html = render_report_html(
        title="주간 경제 심층 브리핑",
        subtitle=f"수집 기준일: {today}",
        body_markdown=report_md,
    )
    send_email(subject, plain_body=report_md, html_body=html)

    # 아카이브 저장 (repo/reports/weekly/에 커밋되도록 워크플로우에서 처리)
    os.makedirs("reports/weekly", exist_ok=True)
    with open(f"reports/weekly/{today}.md", "w", encoding="utf-8") as f:
        f.write(f"# 주간 경제 브리핑 ({today})\n\n{report_md}\n")


if __name__ == "__main__":
    main()
