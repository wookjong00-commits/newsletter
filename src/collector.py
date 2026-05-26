import feedparser
import requests
from datetime import datetime, timedelta, timezone

KST = timezone(timedelta(hours=9))

RSS_FEEDS = {
    "경제": [
        "https://www.hankyung.com/rss/economy",
        "https://rss.mt.co.kr/mt/news.xml",
        "https://www.mk.co.kr/rss/30000001/",
    ],
    "산업": [
        "https://www.hankyung.com/rss/it",
        "https://www.mk.co.kr/rss/50200011/",
        "https://zdnet.co.kr/rss/",
    ],
    "사회": [
        "https://www.yonhapnewstv.co.kr/rss/",
        "https://rss.hani.co.kr/hani.rss",
        "https://www.chosun.com/arc/outboundfeeds/rss/",
    ],
    "정치": [
        "https://www.yonhapnewstv.co.kr/rss/",
        "https://rss.hani.co.kr/politics/rss.xml",
        "https://www.mk.co.kr/rss/30200030/",
    ],
}

MAX_ARTICLES_PER_CATEGORY = 10


def _is_today(entry) -> bool:
    today = datetime.now(KST).date()
    for attr in ("published_parsed", "updated_parsed"):
        t = getattr(entry, attr, None)
        if t:
            dt = datetime(*t[:6], tzinfo=timezone.utc).astimezone(KST)
            return dt.date() == today
    return True  # 날짜 정보 없으면 포함


def _parse_feed(url: str) -> list[dict]:
    try:
        feed = feedparser.parse(url)
        articles = []
        for entry in feed.entries:
            if not _is_today(entry):
                continue
            articles.append({
                "title": entry.get("title", "").strip(),
                "url": entry.get("link", ""),
                "summary": entry.get("summary", entry.get("description", "")).strip(),
                "source": feed.feed.get("title", url),
            })
        return articles
    except Exception:
        return []


def _deduplicate(articles: list[dict]) -> list[dict]:
    seen = set()
    result = []
    for a in articles:
        key = a["title"][:30]
        if key and key not in seen:
            seen.add(key)
            result.append(a)
    return result


def collect() -> dict[str, list[dict]]:
    result = {}
    for category, feeds in RSS_FEEDS.items():
        articles = []
        for url in feeds:
            articles.extend(_parse_feed(url))
        articles = _deduplicate(articles)[:MAX_ARTICLES_PER_CATEGORY]
        result[category] = articles
    return result
