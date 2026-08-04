"""docs/reports/ 안의 리포트들을 스캔해서 docs/index.html 목록 페이지를 만든다."""

import os

DOCS_DIR = "docs"
WEEKLY_DIR = os.path.join(DOCS_DIR, "reports", "weekly")
DAILY_DIR = os.path.join(DOCS_DIR, "reports", "daily")


def _list_reports(directory):
    if not os.path.isdir(directory):
        return []
    files = [f for f in os.listdir(directory) if f.endswith(".html")]
    files.sort(reverse=True)
    return files


def _render_list(files, base_path, empty_label):
    if not files:
        return f"<p class='empty'>아직 {empty_label}가 없습니다.</p>"
    items = "\n".join(
        f'<li><a href="{base_path}/{f}">{f.replace(".html", "")}</a></li>'
        for f in files
    )
    return f"<ul>{items}</ul>"


def build_index():
    weekly_files = _list_reports(WEEKLY_DIR)
    daily_files = _list_reports(DAILY_DIR)

    html = f"""<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>경제 브리핑 아카이브</title>
<link rel="apple-touch-icon" href="apple-touch-icon.png">
<link rel="icon" type="image/png" sizes="32x32" href="favicon-32.png">
<link rel="manifest" href="manifest.json">
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-title" content="경제 브리핑">
<meta name="theme-color" content="#1a2b4c">
<style>
  body {{
    font-family: -apple-system, "Apple SD Gothic Neo", "Malgun Gothic", sans-serif;
    background:#f4f5f7; margin:0; padding:24px; color:#222;
  }}
  .wrapper {{ max-width:680px; margin:0 auto; }}
  h1 {{ color:#1a2b4c; }}
  h2 {{
    color:#2c4a7c; border-left:4px solid #2c4a7c;
    padding-left:10px; margin-top:32px;
  }}
  ul {{ list-style:none; padding:0; }}
  li {{ margin:8px 0; }}
  a {{
    text-decoration:none; color:#1a2b4c; background:#fff;
    display:block; padding:12px 16px; border-radius:8px;
    box-shadow:0 1px 3px rgba(0,0,0,0.08);
  }}
  a:hover {{ background:#eef1f6; }}
  .empty {{ color:#888; }}
</style>
</head>
<body>
<div class="wrapper">
  <h1>경제 브리핑 아카이브</h1>
  <h2>주간 심층 브리핑</h2>
  {_render_list(weekly_files, "reports/weekly", "주간 브리핑")}
  <h2>일일 속보</h2>
  {_render_list(daily_files, "reports/daily", "일일 속보")}
</div>
</body>
</html>
"""
    os.makedirs(DOCS_DIR, exist_ok=True)
    with open(os.path.join(DOCS_DIR, "index.html"), "w", encoding="utf-8") as f:
        f.write(html)


if __name__ == "__main__":
    build_index()
