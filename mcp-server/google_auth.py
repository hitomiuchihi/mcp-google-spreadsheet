# google-auth-oauthlibによる認証処理

# 機能
# 1.	.jsonのクライアントシークレットを読み込む
# 2.	token.json があれば再利用、なければブラウザでOAuth2認証
# 3.	認証後のクライアントでは Sheets / Drive にアクセス可能
# 4.	トークン保存、リフレッシュ

# 使用ライブラリ
# pip install google-auth google-auth-oauthlib google-auth-httplib2 google-api-python-client

import os
import json
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

from config import CLIENT_SECRET_PATH, TOKEN_PATH

# Google APIのスコープ（DriveとSheetsを使う）
SCOPES = [
    "https://www.googleapis.com/auth/drive",
    "https://www.googleapis.com/auth/spreadsheets"
]

def get_google_credentials(creds_path=CLIENT_SECRET_PATH, token_path=TOKEN_PATH):
    """
    Googleの認証情報を取得し、トークンがあれば再利用し、なければブラウザ認証を行う
    """
    creds = None

    if os.path.exists(token_path):
        creds = Credentials.from_authorized_user_file(token_path, SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(creds_path, SCOPES)
            creds = flow.run_local_server(port=8080)

        # トークンを保存
        with open(token_path, 'w') as token:
            token.write(creds.to_json())

    return creds

def get_sheets_service():
    """
    認証済みの Google Sheets API サービスを返す
    """
    creds = get_google_credentials()
    service = build('sheets', 'v4', credentials=creds)
    return service

def get_drive_service():
    """
    認証済みの Google Drive API サービスを返す
    """
    creds = get_google_credentials()
    service = build('drive', 'v3', credentials=creds)
    return service
