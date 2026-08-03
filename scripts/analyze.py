"""
수집된 데이터를 Claude API에 넘겨 분석 텍스트를 생성한다.
- mode="weekly": 주간 심층 브리핑 (긴 종합 분석)
- mode="daily": 조건부 일일 속보 (짧은 1~2문단)
"""

import os
import json
import anthropic

client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])

SYSTEM_PROMPT = """당신은 경제 데이터를 비전문가도 이해할 수 있게 쉽게 풀어서 설명하는 해설자입니다.
반드시 지켜야 할 규칙:
- 전문용어(예: 기준금리, 국채금리, 달러인덱스 등)가 나오면 처음 등장할 때 괄호로 짧게 뜻을 풀어준다.
  예: "기준금리(중앙은행이 은행 간 자금 거래에 적용하는 정책 금리)"
- 숫자와 표보다 "그래서 이게 무슨 뜻인지"를 문장으로 풀어서 설명하는 데 중점을 둔다.
- 확정적인 "매수하라/매도하라/지금 사라/지금 팔아라" 같은 투자 지시는 절대 하지 않는다.
- 대신 "이런 흐름일 때 사람들이 일반적으로 점검하는 것들", "이런 국면에서 고려해볼 만한 대비 방향"처럼
  선택지를 제시하는 형태로 조언한다. 확정적 결론이 아니라 "고려해볼 만한 점"으로 표현한다.
- 데이터가 비어있는 항목은 "데이터 없음"이라고 명시하고 추측하지 않는다.
- 마지막에 "본 내용은 투자 자문이 아니며, 참고용 정보이니 최종 판단과 책임은 본인에게 있습니다"라는
  문구를 반드시 포함한다.
- 한국어로, 친근하고 쉬운 말투로 작성한다.
"""


def generate_weekly_report(data: dict) -> str:
    prompt = f"""아래는 이번 주 수집된 경제 데이터입니다 (JSON):

{json.dumps(data, ensure_ascii=False, indent=2)}

다음 구성으로, 경제 지식이 많지 않은 일반인도 이해할 수 있는 쉬운 말로 주간 브리핑을 작성해주세요:

1. 금리 이야기 (미국/한국) — 무슨 일이 있었고, 그게 왜 중요한지
2. 환율 이야기 (원/달러, 달러인덱스) — 원화가 강해졌는지 약해졌는지, 그게 일상에 어떤 의미인지
3. 주요 지수 이야기 (코스피, S&P500) — 시장 분위기가 어땠는지
4. 이번 주 종합 정리 — 위 내용을 한 문단으로 쉽게 요약
5. 앞으로 대비 방향에 대해 고려해볼 점 — "지금 이런 상황이니, 이런 부분들을 한 번쯤 점검해보면 좋다"는
   식으로 2~4가지 정도, 구체적 종목이나 확정적 매수/매도 지시 없이 제시 (예: 환율 변동에 따른 환헤지 상품
   점검, 금리 국면에 따른 예금·채권 비중 재점검, 분산투자 원칙 재확인 등 일반적으로 고려되는 방향)

위 5개 항목을 모두 빠짐없이 포함해서 작성해주세요. 각 항목은 간결하게 쓰되, 중간에 끊기지 않도록 전체
분량을 조절해주세요.
"""
    msg = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=3000,
        system=SYSTEM_PROMPT,
        messages=[{"role": "user", "content": prompt}],
    )
    return msg.content[0].text


def generate_daily_alert(data: dict, triggered_reasons: list) -> str:
    prompt = f"""오늘 아래 조건이 감지되어 속보를 발송합니다: {triggered_reasons}

관련 데이터 (JSON):
{json.dumps(data, ensure_ascii=False, indent=2)}

쉬운 말로 2~3문단으로 설명해주세요:
1. 무슨 일이 있었는지, 왜 이런 변동이 생겼을 가능성이 있는지 (배경)
2. 이런 상황에서 한 번쯤 점검해보면 좋을 점 1~2가지 (확정적 매수/매도 지시 없이, "고려해볼 만한" 형태로)
"""
    msg = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=500,
        system=SYSTEM_PROMPT,
        messages=[{"role": "user", "content": prompt}],
    )
    return msg.content[0].text
