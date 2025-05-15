# Sheets API操作（gspread or google-api-python-client）

from google_auth import get_drive_service, get_sheets_service
from mcp.types import TextContent
import os

# .env から取得する前提で環境変数使用可（dotenv 経由）
FOLDER_ID = os.getenv("GOOGLE_DRIVE_FOLDER_ID")  # 任意で使う

def get_spreadsheet_id_by_name(spreadsheet_name, folder_id=None):
    """get_spreadsheet_id_by_name
    Google Driveからスプレッドシート名でIDを取得
    Args:
        spreadsheet_name: スプレッドシートのファイル名
        folder_id: Googleドライブのフォルダ名（初期値設定あり）
    """
    drive_service = get_drive_service()

    query_parts = [
        f"name = '{spreadsheet_name}'",
        "mimeType = 'application/vnd.google-apps.spreadsheet'",
        "trashed = false"
    ]
    if folder_id:
        query_parts.insert(0, f"'{folder_id}' in parents")

    query = " and ".join(query_parts)

    response = drive_service.files().list(
        q=query,
        fields="files(id, name)",
        supportsAllDrives=True,
        includeItemsFromAllDrives=True
    ).execute()

    files = response.get("files", [])
    if not files:
        raise Exception(f"Spreadsheet '{spreadsheet_name}' not found")

    return files[0]["id"]



def get_sheet_id_by_name(spreadsheet_id, sheet_name):
    """get_sheet_id_by_name
    スプレッドシートIDとシート名からシートIDを取得
    Args: 
        spreadsheet_name: スプレッドシートのファイル名
        sheet_name: シート名
    """
    sheets_service = get_sheets_service()
    spreadsheet = sheets_service.spreadsheets().get(spreadsheetId=spreadsheet_id).execute()
    for sheet in spreadsheet.get("sheets", []):
        if sheet["properties"]["title"] == sheet_name:
            return sheet["properties"]["sheetId"]
    raise Exception(f"Sheet '{sheet_name}' not found in spreadsheet ID '{spreadsheet_id}'")


async def get_sheet_data(spreadsheet_name, sheet_name="シート1", range_=None):
    """get_sheet_data
    スプレッドシートの特定のシートとからデータを取得する関数（デフォルト: "シート1"）
    Args:
        spreadsheet_name: スプレッドシートのファイル名
        sheet_name: シート名（初期値設定あり）
        range: 範囲
    """
    spreadsheet_id = get_spreadsheet_id_by_name(spreadsheet_name, folder_id=FOLDER_ID)
    sheets_service = get_sheets_service()

    full_range = sheet_name if not range_ else f"{sheet_name}!{range_}"

    result = sheets_service.spreadsheets().values().get(
        spreadsheetId=spreadsheet_id,
        range=full_range
    ).execute()

    return [TextContent(type="text", text=str(result.get("values", [])))]



async def get_all_sheets_data(spreadsheet_name):
    """get_all_sheets_data
    スプレッドシート内のすべてのシートデータを取得する関数
    Args:
        spreadsheet_name: スプレッドシートのファイル名
    """
    spreadsheet_id = get_spreadsheet_id_by_name(spreadsheet_name, folder_id=FOLDER_ID)
    sheets_service = get_sheets_service()

    spreadsheet = sheets_service.spreadsheets().get(spreadsheetId=spreadsheet_id).execute()
    sheet_data = {}

    for sheet in spreadsheet.get("sheets", []):
        title = sheet["properties"]["title"]
        result = sheets_service.spreadsheets().values().get(
            spreadsheetId=spreadsheet_id,
            range=title
        ).execute()
        sheet_data[title] = result.get("values", [])

    return [TextContent(type="text", text=str(sheet_data))]


async def search_records_by_keyword(spreadsheet_name, keyword):
    """get_records_by_keyword
    スプレッドシート全体からキーワードを含む行を抽出する関数 
    Args:
        spreadsheet_name: スプレッドシートのファイル名
        keyword: キーワード
    """
    spreadsheet_id = get_spreadsheet_id_by_name(spreadsheet_name, folder_id=FOLDER_ID)
    sheets_service = get_sheets_service()
    spreadsheet = sheets_service.spreadsheets().get(spreadsheetId=spreadsheet_id).execute()
    matched = {}
    keyword_lower = keyword.lower()

    for sheet in spreadsheet.get("sheets", []):
        title = sheet["properties"]["title"]
        result = sheets_service.spreadsheets().values().get(
            spreadsheetId=spreadsheet_id,
            range=title
        ).execute()
        rows = result.get("values", [])
        filtered_rows = [row for row in rows if any(isinstance(cell, str) and keyword_lower in cell.lower() for cell in row)]
        if filtered_rows:
            matched[title] = filtered_rows

    return [TextContent(type="text", text=str(matched))]


def convert_to_dict_records(values):
    """convert_to_dict_records
    2次元配列またはシート群を辞書形式に変換する関数
    単一シート（2次元リスト） or 複数シート（{sheet_name: 2D list}）両方対応
    [['社名', '業種', ...], [...], ...] → [{社名: A, 業種: IT, ...}, {...}, ...]
    
    Args:
        values: 二次元配列に変換したい値
    """
    if isinstance(values, dict):
        result = {}
        for sheet_name, rows in values.items():
            result[sheet_name] = convert_to_dict_records(rows)
        return result

    if not values or len(values) < 2:
        return []

    headers = values[0]
    records = []

    for row in values[1:]:
        record = {headers[i]: row[i] if i < len(row) else "" for i in range(len(headers))}
        records.append(record)

    return records
