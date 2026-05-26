import os
import replicate

MODEL = "anthropic/claude-opus-4.6"

SYSTEM_PROMPT = """너는 경제·사회·산업·정치 뉴스를 분석하는 전문 편집자다.
주어진 기사 목록을 읽고, 오늘 꼭 알아야 할 핵심 이슈를 간결하게 정리한다.
응답은 반드시 한국어로 작성한다."""


def _run_claude(prompt: str) -> str:
    output = replicate.run(
        MODEL,
        input={
            "system_prompt": SYSTEM_PROMPT,
            "prompt": prompt,
            "max_tokens": 1500,
        },
    )
    return "".join(output)


def summarize_category(category: str, articles: list[dict]) -> dict:
    if not articles:
        return {"category": category, "summary": "오늘 수집된 기사가 없습니다.", "top_articles": []}

    article_text = "\n\n".join(
        f"[{i+1}] {a['title']}\n{a['summary'][:200]}"
        for i, a in enumerate(articles)
    )

    prompt = f"""[{category}] 카테고리 기사 {len(articles)}건입니다.

{article_text}

위 기사들을 바탕으로 다음 형식으로 작성하세요:

## 오늘의 핵심 이슈 (2~3줄)
(가장 중요한 이슈를 2~3문장으로 요약)

## 주요 뉴스
1. (제목): (1~2문장 요약)
2. (제목): (1~2문장 요약)
3. (제목): (1~2문장 요약)

## 투자자 관점 한마디
(이 카테고리의 뉴스가 투자에 미치는 영향 1~2문장)"""

    summary = _run_claude(prompt)

    top_articles = articles[:5]
    return {
        "category": category,
        "summary": summary,
        "top_articles": top_articles,
    }


def summarize_all(news_by_category: dict[str, list[dict]]) -> list[dict]:
    results = []
    for category, articles in news_by_category.items():
        print(f"  [{category}] 요약 중... ({len(articles)}건)")
        result = summarize_category(category, articles)
        results.append(result)
    return results
