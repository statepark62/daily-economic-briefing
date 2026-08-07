import os
from datetime import datetime

from fetch_data import collect_all
from analyze import generate_weekly_report
from html_template import render_report_html
from build_index import build_index
from history import append_history


def main():
    data = collect_all()
    append_history(data)

    report_md = generate_weekly_report(data)

    today = datetime.utcnow().strftime("%Y-%m-%d")

    html = render_report_html(
        title="주간 경제 심층 브리핑",
        subtitle=f"수집 기준일: {today}",
        body_markdown=report_md,
    )

    out_dir = "docs/reports/weekly"
    os.makedirs(out_dir, exist_ok=True)
    with open(f"{out_dir}/{today}.html", "w", encoding="utf-8") as f:
        f.write(html)

    build_index()
    print(f"저장 완료: {out_dir}/{today}.html")


if __name__ == "__main__":
    main()
