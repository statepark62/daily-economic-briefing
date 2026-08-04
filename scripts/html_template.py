"""마크다운 텍스트를 '보고서'처럼 보이는 HTML 이메일로 감싸는 템플릿."""

import markdown as md


def render_report_html(title: str, subtitle: str, body_markdown: str) -> str:
    body_html = md.markdown(body_markdown, extensions=["tables"])

    return f"""\
<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<link rel="apple-touch-icon" href="/daily-economic-briefing/apple-touch-icon.png">
<link rel="icon" type="image/png" sizes="32x32" href="/daily-economic-briefing/favicon-32.png">
<link rel="shortcut icon" href="/daily-economic-briefing/favicon.ico">
<meta name="theme-color" content="#1a2b4c">
<style>
  body {{
    font-family: -apple-system, "Apple SD Gothic Neo", "Malgun Gothic", sans-serif;
    background-color: #f4f5f7;
    margin: 0;
    padding: 0;
    color: #222;
  }}
  .wrapper {{
    max-width: 680px;
    margin: 0 auto;
    padding: 24px 16px;
  }}
  .card {{
    background: #ffffff;
    border-radius: 12px;
    overflow: hidden;
    box-shadow: 0 1px 3px rgba(0,0,0,0.08);
  }}
  .header {{
    background: linear-gradient(135deg, #1a2b4c, #2c4a7c);
    color: #ffffff;
    padding: 28px 28px 22px 28px;
  }}
  .header h1 {{
    margin: 0 0 6px 0;
    font-size: 22px;
  }}
  .header p {{
    margin: 0;
    font-size: 13px;
    opacity: 0.85;
  }}
  .content {{
    padding: 28px;
    font-size: 15px;
    line-height: 1.7;
  }}
  .content h1 {{
    font-size: 19px;
    border-bottom: 2px solid #1a2b4c;
    padding-bottom: 8px;
    margin-top: 32px;
  }}
  .content h2 {{
    font-size: 17px;
    color: #1a2b4c;
    margin-top: 28px;
    border-left: 4px solid #2c4a7c;
    padding-left: 10px;
  }}
  .content h3 {{
    font-size: 15px;
    color: #2c4a7c;
    margin-top: 20px;
  }}
  .content table {{
    border-collapse: collapse;
    width: 100%;
    margin: 12px 0 20px 0;
    font-size: 13px;
  }}
  .content th, .content td {{
    border: 1px solid #e2e5ea;
    padding: 8px 10px;
    text-align: left;
  }}
  .content th {{
    background: #f0f2f6;
  }}
  .content strong {{
    color: #b0361f;
  }}
  .footer {{
    padding: 18px 28px;
    background: #f0f2f6;
    font-size: 12px;
    color: #777;
    line-height: 1.6;
  }}
</style>
</head>
<body>
  <div class="wrapper">
    <div class="card">
      <div class="header">
        <h1>{title}</h1>
        <p>{subtitle}</p>
      </div>
      <div class="content">
        {body_html}
      </div>
      <div class="footer">
        본 내용은 투자 자문이 아니며 참고용 정보입니다. 최종 판단과 책임은 본인에게 있습니다.<br>
        자동 생성 · daily-economic-briefing
      </div>
    </div>
  </div>
</body>
</html>
"""
