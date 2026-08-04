import os
from datetime import datetime

from fetch_data import collect_all
from analyze import generate_daily_alert
from html_template import render_report_html
from build_index import build_index

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
        print("조건 미충족 — 오늘은 속보 페이지를 만들지 않습니다.")
        return

    alert_md = generate_daily_alert(data, triggered)

    today = datetime.utcnow().strftime("%Y-%m-%d")

    html = render_report_html(
        title="일일 경제 속보",
        subtitle=f"감지 항목: {', '.join(triggered)}",
        body_markdown=alert_md,
    )

    out_dir = "docs/reports/daily"
    os.makedirs(out_dir, exist_ok=True)
    with open(f"{out_dir}/{today}.html", "w", encoding="utf-8") as f:
        f.write(html)

    build_index()
    print(f"저장 완료: {out_dir}/{today}.html")


if __name__ == "__main__":
    main()
