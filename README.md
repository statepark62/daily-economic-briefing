# daily-economic-briefing

주요국 금리·환율·경제동향을 자동으로 수집·분석해서 이메일로 보내주는 GitHub Actions 자동화입니다.

- **주 1회 심층 브리핑**: 매주 월요일(한국시간 07:00) 금리/환율/지수 종합 분석 이메일 발송
- **매일 조건부 속보**: 매일 체크하되, 환율·지수 등이 임계값 이상 변동한 날에만 짧은 속보 발송

## 설정 방법

1. 이 저장소 **Settings → Secrets and variables → Actions**에서 아래 값 등록
   - `ANTHROPIC_API_KEY`
   - `FRED_API_KEY` (https://fred.stlouisfed.org/docs/api/api_key.html 에서 무료 발급)
   - `ECOS_API_KEY` (https://ecos.bok.or.kr 에서 무료 발급, 없으면 한국 기준금리 항목만 비어서 나감)
   - `MAIL_USERNAME` (발신용 Gmail 주소)
   - `MAIL_PASSWORD` (Gmail **앱 비밀번호** — 일반 로그인 비밀번호 아님)
   - `MAIL_TO` (리포트 받을 이메일 주소)

2. **Settings → Actions → General → Workflow permissions**에서
   "Read and write permissions"로 설정 (리포트 아카이브를 자동 커밋하려면 필요)

3. 워크플로우는 기본적으로 스케줄대로 자동 실행되지만,
   **Actions 탭 → 원하는 워크플로우 → Run workflow** 버튼으로 즉시 테스트 실행 가능

## 조건부 속보 임계값 조정

`scripts/run_daily.py`의 `THRESHOLDS` 딕셔너리에서 환율/지수 변동 기준(%)을 조정할 수 있습니다.

## 주의

본 자동화가 생성하는 내용은 투자 자문이 아니며, 공개된 경제 데이터를 객관적으로 요약·해설하는 참고용 정보입니다.
