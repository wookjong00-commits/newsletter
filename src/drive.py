import os
from pathlib import Path

DOCS_DIR = Path(__file__).parent.parent / "docs"


def save_html(html: str, filename: str) -> str:
    DOCS_DIR.mkdir(exist_ok=True)
    path = DOCS_DIR / filename
    path.write_text(html, encoding="utf-8")

    # index.html → 최신 뉴스레터로 리다이렉트
    index = DOCS_DIR / "index.html"
    index.write_text(
        f'<!DOCTYPE html><html><head><meta charset="UTF-8">'
        f'<meta http-equiv="refresh" content="0;url={filename}"></head>'
        f'<body><a href="{filename}">최신 뉴스레터 열기</a></body></html>',
        encoding="utf-8",
    )

    print(f"  HTML 저장: docs/{filename}")
    return str(path)
