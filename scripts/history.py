"""
매 실행 시 수집된 데이터를 docs/data/history.json에 날짜별로 누적 저장한다.
차트 페이지(docs/trends.html)가 이 파일을 읽어서 그래프를 그린다.
"""

import json
import os
from datetime import datetime

HISTORY_PATH = "docs/data/history.json"


def _latest_value(series):
    """FRED/ECOS API가 반환하는 [(date, value), ...] 형태에서 최신 값만 float으로 추출."""
    if not series:
        return None
    try:
        return float(series[0][1])
    except (IndexError, ValueError, TypeError):
        return None


def append_history(data: dict):
    market = data.get("market", {})

    record = {
        "date": datetime.utcnow().strftime("%Y-%m-%d"),
        "usd_krw": market.get("USD_KRW", {}).get("latest"),
        "dxy": market.get("DXY", {}).get("latest"),
        "kospi": market.get("KOSPI", {}).get("latest"),
        "sp500": market.get("SP500", {}).get("latest"),
        "fed_funds_rate": _latest_value(data.get("fed_funds_rate")),
        "kr_base_rate": _latest_value(data.get("kr_base_rate")),
    }

    os.makedirs(os.path.dirname(HISTORY_PATH), exist_ok=True)

    history = []
    if os.path.exists(HISTORY_PATH):
        with open(HISTORY_PATH, "r", encoding="utf-8") as f:
            try:
                history = json.load(f)
            except json.JSONDecodeError:
                history = []

    # 같은 날짜 기록이 이미 있으면 최신 값으로 덮어쓰고, 없으면 새로 추가
    history = [h for h in history if h.get("date") != record["date"]]
    history.append(record)
    history.sort(key=lambda h: h["date"])

    with open(HISTORY_PATH, "w", encoding="utf-8") as f:
        json.dump(history, f, ensure_ascii=False, indent=2)

    print(f"history.json 갱신 완료 (총 {len(history)}개 날짜 기록)")
