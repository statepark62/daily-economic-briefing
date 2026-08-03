"""
수집된 데이터를 Claude API에 넘겨 분석 텍스트를 생성한다.
- mode="weekly": 주간 심층 브리핑 (긴 종합 분석)
- mode="daily": 조건부 일일 속보 (짧은 1~2문단)
"""

import os
import json
import anthropic

client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])

SYSTEM_PROMPT = """당신은 경제 데이터를 객관적으로 해설하는 애널리스트입니다.
반드시 지켜야 할 규칙:
- 확정적인 "매수하라/매도하라" 같은 투자 지시는 절대 하지 않는다.
- 대신 "이런 데이터가 이런 배경에서 나왔다", "역사적으로 이런 국면에서는 이런 흐름이 있었다" 같은
  객관적 설명과 시사점 위주로 작성한다.
- 데이터가 비어있는 항목은 "데이터 없음"이라고 명시하고 추측하지 않는다.
- 마지막에 "본 내용은 투자 자문이 아니며 참고용 정보입니다"라는 문구를 반드시 포함한다.
- 한국어로 작성한다.
"""


def generate_weekly_report(data: dict) -> str:
    prompt = f"""아래는 이번 주 수집된 경제 데이터입니다 (JSON):

{json.dumps(data, ensure_ascii=False, indent=2)}

다음 구성으로 주간 심층 브리핑을 작성해주세요:
1. 금리 동향 (미국/한국)
2. 환율 동향 (원/달러, 달러인덱스)
3. 주요 지수 동향 (코스피, S&P500)
4. 이번 주 종합 시사점 (투자 지시가 아닌 객관적 해설)
"""
    msg = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=1500,
        system=SYSTEM_PROMPT,
        messages=[{"role": "user", "content": prompt}],
    )
    return msg.content[0].text


def generate_daily_alert(data: dict, triggered_reasons: list) -> str:
    prompt = f"""오늘 아래 조건이 감지되어 속보를 발송합니다: {triggered_reasons}

관련 데이터 (JSON):
{json.dumps(data, ensure_ascii=False, indent=2)}

이 변동에 대해 1~2문단으로 짧게 객관적으로 설명해주세요. 배경과 참고할 만한 맥락 위주로 작성하고,
투자 지시는 하지 마세요.
"""
    msg = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=500,
        system=SYSTEM_PROMPT,
        messages=[{"role": "user", "content": prompt}],
    )
    return msg.content[0].text
