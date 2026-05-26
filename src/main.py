import os
from dotenv import load_dotenv

load_dotenv()

from collector import collect
from summarizer import summarize_all
from sheets import append_articles
from renderer import render
from drive import upload_html


def main():
    print("=== 뉴스레터 생성 시작 ===")

    print("\n[1/4] 뉴스 수집 중...")
    news = collect()
    total = sum(len(v) for v in news.values())
    print(f"  총 {total}건 수집 완료")

    print("\n[2/4] Claude로 요약 중...")
    summaries = summarize_all(news)

    print("\n[3/4] Google Sheets 저장 중...")
    append_articles(summaries)

    print("\n[4/4] HTML 생성 및 Drive 업로드 중...")
    html, filename = render(summaries)
    file_id = upload_html(html, filename)

    print(f"\n=== 완료 ===")
    print(f"파일명: {filename}")
    print(f"Drive 파일 ID: {file_id}")
    print(f"링크: https://drive.google.com/file/d/{file_id}/view")


if __name__ == "__main__":
    main()
