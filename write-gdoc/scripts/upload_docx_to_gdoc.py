#!/usr/bin/env python3
"""
upload_docx_to_gdoc.py

Upload a local .docx to Google Drive with MIME conversion so Drive stores it
as a native Google Doc (Title style, headings, tables, bullets all preserved
from the docx).

Uses the standard Google API Python client with OAuth user credentials.

SETUP (one-time):
    pip install google-api-python-client google-auth-httplib2 google-auth-oauthlib

    1. Create an OAuth 2.0 Client ID (Desktop app) in Google Cloud Console:
       https://console.cloud.google.com/apis/credentials
    2. Download the JSON to ~/.config/gdoc-upload/credentials.json
       (or override with --credentials).
    3. Enable the Google Drive API for the same project.
    4. First run will open a browser for consent and cache a token at
       ~/.config/gdoc-upload/token.json.

USAGE:
    upload_docx_to_gdoc.py \\
        --docx /abs/path/to/file.docx \\
        --folder-id <drive_folder_id> \\
        --title "Doc Title"

    # Or via the wrapper:
    upload_docx_to_gdoc.sh --docx ... --folder-id ... --title ...
"""
from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path

try:
    from google.auth.transport.requests import Request  # type: ignore
    from google.oauth2.credentials import Credentials  # type: ignore
    from google_auth_oauthlib.flow import InstalledAppFlow  # type: ignore
    from googleapiclient.discovery import build  # type: ignore
    from googleapiclient.http import MediaFileUpload  # type: ignore
except ImportError as e:
    sys.stderr.write(
        "ERROR: Missing Google API client libraries. Install with:\n"
        "  pip install google-api-python-client google-auth-httplib2 "
        "google-auth-oauthlib\n\n"
        f"Import error: {e}\n"
    )
    sys.exit(2)


DOCX_MIME = "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
GDOC_MIME = "application/vnd.google-apps.document"
SCOPES = ["https://www.googleapis.com/auth/drive.file"]

DEFAULT_CONFIG_DIR = Path(os.environ.get("GDOC_UPLOAD_CONFIG", "~/.config/gdoc-upload")).expanduser()
DEFAULT_CREDENTIALS = DEFAULT_CONFIG_DIR / "credentials.json"
DEFAULT_TOKEN = DEFAULT_CONFIG_DIR / "token.json"


def get_credentials(credentials_path: Path, token_path: Path) -> Credentials:
    creds: Credentials | None = None
    if token_path.exists():
        creds = Credentials.from_authorized_user_file(str(token_path), SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            if not credentials_path.exists():
                raise FileNotFoundError(
                    f"OAuth client credentials not found at {credentials_path}. "
                    "Create an OAuth 2.0 Client ID (Desktop app) in Google Cloud "
                    "Console and save the JSON to that path."
                )
            flow = InstalledAppFlow.from_client_secrets_file(str(credentials_path), SCOPES)
            creds = flow.run_local_server(port=0)
        token_path.parent.mkdir(parents=True, exist_ok=True)
        token_path.write_text(creds.to_json())

    return creds


def upload(
    docx_path: str,
    folder_id: str,
    title: str | None = None,
    credentials_path: Path = DEFAULT_CREDENTIALS,
    token_path: Path = DEFAULT_TOKEN,
) -> dict:
    docx = Path(docx_path).expanduser().resolve()
    if not docx.exists():
        raise FileNotFoundError(f"Not found: {docx}")
    if docx.suffix.lower() != ".docx":
        raise ValueError(f"Expected .docx, got: {docx.suffix}")

    creds = get_credentials(credentials_path, token_path)
    drive = build("drive", "v3", credentials=creds, cache_discovery=False)

    metadata = {
        "name": title or docx.stem,
        "mimeType": GDOC_MIME,
        "parents": [folder_id],
    }
    media = MediaFileUpload(str(docx), mimetype=DOCX_MIME, resumable=True)

    created = (
        drive.files()
        .create(body=metadata, media_body=media, fields="id,name,webViewLink,parents")
        .execute()
    )
    created["url"] = f"https://docs.google.com/document/d/{created['id']}/edit"
    return created


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--docx", required=True, help="Absolute path to local .docx file")
    ap.add_argument("--folder-id", required=True, help="Target Google Drive folder ID")
    ap.add_argument("--title", help="Doc title in Drive (defaults to docx stem)")
    ap.add_argument(
        "--credentials",
        default=str(DEFAULT_CREDENTIALS),
        help=f"Path to OAuth client credentials JSON (default: {DEFAULT_CREDENTIALS})",
    )
    ap.add_argument(
        "--token",
        default=str(DEFAULT_TOKEN),
        help=f"Path to cached OAuth token JSON (default: {DEFAULT_TOKEN})",
    )
    args = ap.parse_args()

    result = upload(
        args.docx,
        args.folder_id,
        args.title,
        Path(args.credentials).expanduser(),
        Path(args.token).expanduser(),
    )
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
