import os
import io
import json
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseUpload

SCOPES = [
    "https://www.googleapis.com/auth/drive.file",
]


def _get_service():
    raw = os.environ["GOOGLE_SERVICE_ACCOUNT_JSON"]
    info = json.loads(raw)
    creds = Credentials.from_service_account_info(info, scopes=SCOPES)
    return build("drive", "v3", credentials=creds)


def upload_html(html: str, filename: str) -> str:
    folder_id = os.environ["GOOGLE_DRIVE_FOLDER_ID"]
    service = _get_service()

    content = html.encode("utf-8")
    media = MediaIoBaseUpload(io.BytesIO(content), mimetype="text/html", resumable=False)
    metadata = {"name": filename, "parents": [folder_id]}

    # 같은 날짜 파일이 있으면 덮어쓰기
    existing = service.files().list(
        q=f"name='{filename}' and '{folder_id}' in parents and trashed=false",
        fields="files(id)",
    ).execute().get("files", [])

    if existing:
        file_id = existing[0]["id"]
        service.files().update(fileId=file_id, media_body=media).execute()
        print(f"  Drive 업데이트: {filename}")
        return file_id
    else:
        file = service.files().create(body=metadata, media_body=media, fields="id").execute()
        print(f"  Drive 업로드: {filename}")
        return file["id"]
