import os
import io
import json
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseUpload

SCOPES = ["https://www.googleapis.com/auth/drive.file"]
DOC_MIME = "application/vnd.google-apps.document"


def _get_service():
    raw = os.environ["GOOGLE_SERVICE_ACCOUNT_JSON"]
    info = json.loads(raw)
    creds = Credentials.from_service_account_info(info, scopes=SCOPES)
    return build("drive", "v3", credentials=creds)


def upload_html(html: str, filename: str) -> str:
    folder_id = os.environ["GOOGLE_DRIVE_FOLDER_ID"]
    service = _get_service()

    # Google Doc으로 변환 업로드 (서비스 계정은 스토리지 쿼터 없음 → Doc은 쿼터 미사용)
    doc_name = filename.replace(".html", "")
    content = html.encode("utf-8")
    media = MediaIoBaseUpload(io.BytesIO(content), mimetype="text/html", resumable=False)
    metadata = {"name": doc_name, "parents": [folder_id], "mimeType": DOC_MIME}

    existing = service.files().list(
        q=f"name='{doc_name}' and '{folder_id}' in parents and trashed=false",
        fields="files(id)",
    ).execute().get("files", [])

    if existing:
        file_id = existing[0]["id"]
        service.files().update(fileId=file_id, media_body=media).execute()
        print(f"  Drive 업데이트: {doc_name}")
    else:
        file = service.files().create(
            body=metadata, media_body=media, fields="id"
        ).execute()
        file_id = file["id"]
        print(f"  Drive 업로드 (Google Doc): {doc_name}")

    return file_id
