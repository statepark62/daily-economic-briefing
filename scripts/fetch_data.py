"""
금리 / 환율 / 주요 지수 데이터를 수집해서 dict로 반환하는 모듈.
- FRED: 미국 기준금리, 10년물 국채금리, CPI
- 한국은행 ECOS: 한국 기준금리 (ECOS_API_KEY 없으면 건너뜀)
- yfinance: 환율(USD/KRW), 달러인덱스, 코스피, S&P500
"""

import os
import requests
import yfinance as yf
from datetime import datetime, timedelta

FRED_API_KEY = os.environ.get("FRED_API_KEY", "")
ECOS_API_KEY = os.environ.get("ECOS_API_KEY", "")


def fetch_fred_series(series_id, limit=2):
    """FRED에서 최근 관측치 N개를 가져온다."""
    if not FRED_API_KEY:
        return []
    url = "https://api.stlouisfed.org/fred/series/observations"
    params = {
        "series_id": series_id,
        "api_key": FRED_API_KEY,
        "file_type": "json",
        "sort_order": "desc",
        "limit": limit,
    }
    try:
        r = requests.get(url, params=params, timeout=15)
        r.raise_for_status()
        obs = r.json().get("observations", [])
        return [(o["date"], o["value"]) for o in obs if o["value"] != "."]
    except Exception as e:
        print(f"[fred] {series_id} 조회 실패: {e}")
        return []


def fetch_ecos_base_rate():
    """한국은행 기준금리 (ECOS API). 최근 1개월 범위로 조회."""
    if not ECOS_API_KEY:
        return []
    end = datetime.utcnow()
    start = end - timedelta(days=60)
    stat_code = "722Y001"  # 한국은행 기준금리 통계표 코드
    item_code = "0101000"
    url = (
        f"https://ecos.bok.or.kr/api/StatisticSearch/{ECOS_API_KEY}/json/kr/1/10/"
        f"{stat_code}/M/{start.strftime('%Y%m')}/{end.strftime('%Y%m')}/{item_code}"
    )
    try:
        r = requests.get(url, timeout=15)
        r.raise_for_status()
        rows = r.json().get("StatisticSearch", {}).get("row", [])
        return [(row["TIME"], row["DATA_VALUE"]) for row in rows]
    except Exception as e:
        print(f"[ecos] 기준금리 조회 실패: {e}")
        return []


# 하루 변동률로는 현실적으로 나오기 어려운 상한선.
# 이 값을 넘으면 실제 시장 변동이 아니라 데이터 오류(휴장일 비교, 캐시 이상 등)일 가능성이 높다고 보고 제외한다.
MAX_PLAUSIBLE_CHANGE_PCT = {
    "USD_KRW": 5.0,
    "DXY": 3.0,
    "KOSPI": 10.0,   # 코스피 서킷브레이커 1단계가 8%이므로 그 이상은 사실상 데이터 오류
    "SP500": 8.0,
    "KOSDAQ": 12.0,  # 코스닥은 코스피보다 변동성이 커서 상한선을 조금 더 넉넉히 둠
}


def fetch_market_data():
    """yfinance로 환율/지수 최근 2거래일 종가를 가져온다.
    비현실적으로 큰 변동치는 데이터 오류로 간주해 결과에서 제외한다."""
    tickers = {
        "USD_KRW": "KRW=X",
        "DXY": "DX-Y.NYB",
        "KOSPI": "^KS11",
        "KOSDAQ": "^KQ11",
        "SP500": "^GSPC",
    }
    result = {}
    for name, ticker in tickers.items():
        try:
            hist = yf.Ticker(ticker).history(period="5d")
            closes = hist["Close"].dropna()
            if len(closes) < 2:
                continue

            latest = float(closes.iloc[-1])
            prev = float(closes.iloc[-2])
            change_pct = round((latest - prev) / prev * 100, 2)

            limit = MAX_PLAUSIBLE_CHANGE_PCT.get(name, 10.0)
            if abs(change_pct) > limit:
                print(
                    f"[yfinance] {name} 변동률 {change_pct}%가 상한({limit}%)을 초과 — "
                    f"데이터 오류로 판단해 이번 수집에서 제외합니다 (latest={latest}, prev={prev})"
                )
                continue

            result[name] = {
                "latest": round(latest, 2),
                "prev": round(prev, 2),
                "change_pct": change_pct,
            }
        except Exception as e:
            print(f"[yfinance] {name} 조회 실패: {e}")
    return result


def collect_all():
    return {
        "fed_funds_rate": fetch_fred_series("DFF"),
        "us_10y_treasury": fetch_fred_series("DGS10"),
        "us_cpi": fetch_fred_series("CPIAUCSL"),
        "kr_base_rate": fetch_ecos_base_rate(),
        "market": fetch_market_data(),
        "collected_at": datetime.utcnow().isoformat(),
    }


if __name__ == "__main__":
    import json

    print(json.dumps(collect_all(), indent=2, ensure_ascii=False))
