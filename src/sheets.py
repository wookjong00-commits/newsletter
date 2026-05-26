import os
import json
from datetime import datetime, timedelta, timezone
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build

KST = timezone(timedelta(hours=9))
SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]
SHEET_NAME = "뉴스DB"
HEADERS = ["날짜", "카테고리", "제목", "요약", "URL", "출처"]


def _get_service():
    raw = os.environ["GOOGLE_SERVICE_ACCOUNT_JSON"]
    info = json.loads(raw)
    creds = Credentials.from_service_account_info(info, scopes=SCOPES)
    return build("sheets", "v4", credentials=creds)


def _ensure_sheet(service, sheet_id: str):
    meta = service.spreadsheets().get(spreadsheetId=sheet_id).execute()
    names = [s["properties"]["title"] for s in meta["sheets"]]
    if SHEET_NAME not in names:
        service.spreadsheets().batchUpdate(
            spreadsheetId=sheet_id,
            body={"requests": [{"addSheet": {"properties": {"title": SHEET_NAME}}}]},
        ).execute()
        service.spreadsheets().values().update(
            spreadsheetId=sheet_id,
            range=f"{SHEET_NAME}!A1",
            valueInputOption="RAW",
            body={"values": [HEADERS]},
        ).execute()


def append_articles(summaries: list[dict]):
    sheet_id = os.environ["GOOGLE_SHEET_ID"]
    service = _get_service()
    _ensure_sheet(service, sheet_id)

    today = datetime.now(KST).strftime("%Y-%m-%d")
    rows = []
    for s in summaries:
        for article in s["top_articles"]:
            rows.append([
                today,
                s["category"],
                article.get("title", ""),
                article.get("summary", "")[:300],
                article.get("url", ""),
                article.get("source", ""),
            ])

    if not rows:
        return

    service.spreadsheets().values().append(
        spreadsheetId=sheet_id,
        range=f"{SHEET_NAME}!A1",
        valueInputOption="RAW",
        insertDataOption="INSERT_ROWS",
        body={"values": rows},
    ).execute()
    print(f"  Sheets에 {len(rows)}건 저장 완료")
