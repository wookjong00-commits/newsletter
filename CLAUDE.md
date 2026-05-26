# newsletter

생성일: 2026-05-26
경로: /Users/ugg/projects/newsletter

## 역할

너는 이 프로젝트의 전담 개발 파트너다. 사용자와 함께 이 프로젝트를 처음부터 완성까지 이끌어간다.

## 목적

매일 경제, 사회, 산업, 정치 주요 이슈를 RSS로 자동 수집·Claude로 요약하여 뉴스레터를 생성하는 자동화 시스템.

## 현재 아키텍처

```
GitHub Actions (매일 오전 7시 KST, cron: 0 22 * * *)
        ↓
  RSS 수집 (src/collector.py)
  - 경제: 한국경제, 머니투데이, 매일경제
  - 산업: 한국경제IT, 매일경제IT, ZDNet
  - 사회: 연합뉴스, 한겨레, 조선일보
  - 정치: 연합뉴스, 한겨레정치, 매일경제정치
        ↓
  Claude 요약 (src/summarizer.py)
  - 모델: Replicate anthropic/claude-opus-4.6
  - 카테고리별 핵심 이슈 + 투자자 관점 요약
        ↓
    ┌───┴───┐
    ↓       ↓
 Google    HTML
 Sheets   생성
 (원본DB)  (src/renderer.py)
           ↓
      docs/ 폴더에 저장
      GitHub Pages 배포
```

## 파일 구조

```
src/
  collector.py    - RSS 피드 수집 및 날짜 필터링
  summarizer.py   - Replicate Claude API 요약
  sheets.py       - Google Sheets 원본 기사 적재
  renderer.py     - Jinja2 HTML 뉴스레터 렌더링
  drive.py        - HTML을 docs/ 폴더에 저장 (GitHub Pages용)
  main.py         - 파이프라인 오케스트레이터
templates/
  newsletter.html - 뉴스레터 HTML 템플릿
docs/             - GitHub Pages 서빙 폴더
  index.html      - 최신 날짜로 리다이렉트
  YYYY-MM-DD.html - 날짜별 뉴스레터
.github/workflows/
  daily.yml       - GitHub Actions 스케줄러
```

## 배포 정보

- GitHub 레포: https://github.com/wookjong00-commits/newsletter
- 뉴스레터 URL: https://wookjong00-commits.github.io/newsletter/
- Google Sheets: 1XlmMVx3Z2yptfqUJsYBGrB8RUMfM3oZOpbkfawEQ0is

## GitHub Secrets

| 키 | 설명 |
|----|------|
| REPLICATE_API_TOKEN | Replicate API 토큰 |
| GOOGLE_SERVICE_ACCOUNT_JSON | 서비스 계정 JSON (newsletter-bot@newsletter-497514.iam.gserviceaccount.com) |
| GOOGLE_SHEET_ID | Google Sheets ID |
| GOOGLE_DRIVE_FOLDER_ID | Drive 폴더 ID (1RAhZ0tYPeunLQnVdho6231rUT9J4pemF) |

## 알려진 문제 및 TODO

- [ ] RSS 날짜 필터 버그: 기사가 수집되지 않음 (오늘 날짜 매칭 실패)
- [ ] Google Drive 직접 업로드 검토 중 (MCP 쓰기 권한 확인 후 결정)
- [ ] Replicate API 토큰 교체 필요 (채팅에 노출됨)
- [ ] 사회 카테고리 RSS 피드 수집 0건 개선 필요

## 참고 사항

- 상위 목표: 투자 시드 1,000만원으로 1억 수익
- Google Cloud 프로젝트 ID: newsletter-497514
- 서비스 계정: newsletter-bot@newsletter-497514.iam.gserviceaccount.com
