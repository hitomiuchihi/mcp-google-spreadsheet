# main.py - Python版MCPサーバーのエントリーポイント

import os
import sys
import signal
import logging
import asyncio
from mcp.server.fastmcp import FastMCP
from mcp.server.stdio import stdio_server
from mcp.types import TextContent
from google_auth import get_google_credentials

from google_sheet import (
    get_sheet_data,
    get_all_sheets_data,
    search_records_by_keyword,
)


# ログ取得
def get_logger():
    logger = logging.getLogger("mcp-server")
    handler = logging.StreamHandler()
    formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)
    return logger

# サーバーの起動
async def run_server():
    logger = get_logger()
    logger.info("✅ Starting MCP Server...")
    
    # 🔑 認証チェックと初回認証
    try:
        get_google_credentials()  # この時点で認証されていなければブラウザ起動
        logger.info("✅ Google認証チェック完了（token.json 確認済み）")
    except Exception as e:
        logger.error(f"❌ Google認証に失敗しました: {e}")
        return  # サーバー起動せず終了

    # Serverインスタンスの作成（名前だけ指定）
    server = FastMCP("spreadsheet-mcp")
    
    server.tool()(get_sheet_data)
    server.tool()(get_all_sheets_data)
    server.tool()(search_records_by_keyword)

    # 登録されたツール名をログ出力
    print("✅ Registered tools:", [
        func.__name__ for func in [
            get_sheet_data, get_all_sheets_data, search_records_by_keyword
        ]
    ])

    # FastMCPのstdio実行
    await server.run_stdio_async()

def main():
    # Ctrl+C に対応
    def shutdown_handler(sig, frame):
        print("Shutting down MCP server...")
        sys.exit(0)

    signal.signal(signal.SIGINT, shutdown_handler)
    signal.signal(signal.SIGTERM, shutdown_handler)

    asyncio.run(run_server())


if __name__ == "__main__":
    main()
