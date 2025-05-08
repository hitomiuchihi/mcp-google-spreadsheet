# エントリーポイント

from google_auth import get_sheets_service

if __name__ == '__main__':
    sheets_service = get_sheets_service()
    print("✅ Google Sheets API connected successfully!")