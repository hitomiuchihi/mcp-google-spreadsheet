# main.py - Python版MCPサーバーのエントリーポイント

import os
import signal
import sys
import logging
from contextlib import suppress
from mcp import Server
from mcp.transport.stdio import StdioTransport

from google_auth import get_google_credentials
from google_sheet import (
    get_sheet_data,
    get_all_sheets_data,
    search_records_by_keyword,
    # convert_to_dict_records,
)


def get_logger():
    logger = logging.getLogger("mcp-server")
    handler = logging.StreamHandler()
    formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)
    return logger


def main():
    logger = get_logger()

    # graceful shutdown 対応
    def shutdown_handler(sig, frame):
        logger.info("Shutting down MCP server...")
        sys.exit(0)

    signal.signal(signal.SIGINT, shutdown_handler)
    signal.signal(signal.SIGTERM, shutdown_handler)

    logger.info("Starting MCP Server...")
    server = Server(transport=StdioTransport())

    # MCPツール登録
    server.register_tool(
        name="get_sheet_data",
        description="指定したシートのデータを取得する（デフォルトは「シート1」）",
        func=get_sheet_data,
    )
    server.register_tool(
        name="get_all_sheets_data",
        description="スプレッドシート内のすべてのシートデータを取得する",
        func=get_all_sheets_data,
    )
    server.register_tool(
        name="search_records_by_keyword",
        description="スプレッドシート全体からキーワードを含む行を検索する",
        func=search_records_by_keyword,
    )
    # server.register_tool(
    #     name="convert_to_dict_records",
    #     description="スプレッドシートのデータを辞書形式に変換する",
    #     func=convert_to_dict_records,
    # )

    # サーバー起動
    with suppress(KeyboardInterrupt):
        server.serve()


if __name__ == "__main__":
    main()
