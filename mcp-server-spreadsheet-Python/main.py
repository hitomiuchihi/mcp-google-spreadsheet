# main.py - Python版MCPサーバーのエントリーポイント

import signal
import sys
import logging

from google_auth import get_google_credentials
from google_drive import list_files, copy_file, rename_file
from google_sheet import (
    get_sheet_data,
    get_all_sheets_data,
    search_records_by_keyword,
    # 以下に必要に応じて追加予定:
    # copy_sheet_handler,
    # rename_sheet_handler,
    # list_sheets_handler,
    # add_rows_handler,
    # add_columns_handler,
    # update_cells_handler,
    # batch_update_cells_handler,
    # delete_rows_handler,
    # delete_columns_handler,
)

# MCPサーバーとトランスポート
from mcp import Server
from mcp.transport.stdio import StdioTransport

def main():
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger("mcp-server")

    def handle_exit(signum, frame):
        logger.info("Signal received, exiting.")
        sys.exit(0)

    signal.signal(signal.SIGINT, handle_exit)
    signal.signal(signal.SIGTERM, handle_exit)

    # Google認証確認（初回認証も含む）
    try:
        get_google_credentials()
        logger.info("✅ Google authentication succeeded")
    except Exception as e:
        logger.error(f"❌ Failed to authenticate Google: {e}")
        sys.exit(1)

    server = Server(transport=StdioTransport())

    # MCPツール登録（関数名と整合性を合わせて必要に応じて整理）
    server.register_tool("get_sheet_data", "Get data from Google Sheets", get_sheet_data)
    server.register_tool("get_all_sheets_data", "Get all sheets from Google Sheets", get_all_sheets_data)
    server.register_tool("search_records_by_keyword", "Search records across sheets by keyword", search_records_by_keyword)
    # 追加で以下を定義していく:
    # server.register_tool("add_rows", "Add rows to sheet", add_rows_handler)
    # ...

    logger.info("🚀 MCP server starting...")
    server.serve()

if __name__ == "__main__":
    main()
