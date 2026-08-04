"""
이미 생성되어 있는 docs/reports/**/*.html 파일들에
'← 목록으로' 뒤로가기 링크와 관련 CSS를 소급 삽입한다.
한 번만 실행하면 되는 일회성 스크립트.
"""

import glob

BACK_LINK_CSS = """  .back-link {
    display: inline-block;
    color: #ffffff;
    opacity: 0.85;
    text-decoration: none;
    font-size: 13px;
    margin-bottom: 14px;
  }
  .back-link:hover {
    opacity: 1;
    text-decoration: underline;
  }
"""

BACK_LINK_HTML = '        <a class="back-link" href="../../index.html">← 목록으로</a>\n'


def retrofit_file(path: str) -> bool:
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()

    if "back-link" in content:
        return False  # 이미 적용된 파일은 건너뜀

    # 1. CSS 삽입 (</style> 바로 앞)
    if "</style>" in content:
        content = content.replace("</style>", BACK_LINK_CSS + "</style>", 1)

    # 2. 헤더 안에 링크 삽입 (<div class="header"> 바로 다음 줄)
    marker = '<div class="header">'
    if marker in content:
        content = content.replace(marker, marker + "\n" + BACK_LINK_HTML.rstrip("\n"), 1)

    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    return True


def main():
    files = glob.glob("docs/reports/**/*.html", recursive=True)
    updated = 0
    for path in files:
        if retrofit_file(path):
            print(f"수정됨: {path}")
            updated += 1
        else:
            print(f"건너뜀(이미 적용됨): {path}")
    print(f"\n총 {len(files)}개 중 {updated}개 파일에 뒤로가기 링크 추가 완료")


if __name__ == "__main__":
    main()
