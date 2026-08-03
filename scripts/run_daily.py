import os
from datetime import datetime

from fetch_data import collect_all
from analyze import generate_daily_alert
from send_email import send_email
from html_template import render_report_html

# 조건 임계값 (필요에 따라 조정하세요)
THRESHOLDS = {
    "USD_KRW": 1.0,   # %
    "DXY": 0.5,       # %
    "KOSPI": 1.5,     # %
    "SP500": 1.5,     # %
}


def check_conditions(market: dict):
    triggered = []
    for name, threshold in THRESHOLDS.items():
        info = market.get(name)
        if info and abs(info["change_pct"]) >= threshold:
            triggered.append(
                f"{name} {info['change_pct']:+.2f}% (기준 {threshold}% 이상)"
            )
    return triggered


def main():
    data = collect_all()
    triggered = check_conditions(data.get("market", {}))

    if not triggered:
        print("조건 미충족 — 오늘은 속보를 발송하지 않습니다.")
        return

    alert_md = generate_daily_alert(data, triggered)

    today = datetime.utcnow().strftime("%Y-%m-%d")
    subject = f"[속보] 경제 지표 변동 감지 {today}"

    html = render_report_html(
        title="일일 경제 속보",
        subtitle=f"감지 항목: {', '.join(triggered)}",
        body_markdown=alert_md,
    )
    send_email(subject, plain_body=alert_md, html_body=html)

    os.makedirs("reports/daily", exist_ok=True)
    with open(f"reports/daily/{today}.md", "w", encoding="utf-8") as f:
        f.write(f"# 일일 속보 ({today})\n\n트리거: {triggered}\n\n{alert_md}\n")


if __name__ == "__main__":
    main()
