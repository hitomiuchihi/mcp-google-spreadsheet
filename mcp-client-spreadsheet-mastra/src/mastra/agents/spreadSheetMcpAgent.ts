import { openai } from "@ai-sdk/openai"; // OpenAI SDKをインポート
import { Agent } from "@mastra/core/agent";
import { MCPClient } from "@mastra/mcp";

// client secretがない時にアラートを出す場合は以下を使用
if (!process.env.MCPGS_CLIENT_SECRET_PATH) {
  throw new Error("MCPGS_CLIENT_SECRET_PATH is not defined in environment variables");
}

// MCP定義
const mcp = new MCPClient({
	// MCPサーバー情報
  servers: {
    "mcp_google_spreadsheet": {
      command: "mcp-google-spreadsheet",
      args: [],
      env: {
        MCPGS_CLIENT_SECRET_PATH: process.env.MCPGS_CLIENT_SECRET_PATH!,
        MCPGS_TOKEN_PATH: process.env.MCPGS_TOKEN_PATH!,
        MCPGS_FOLDER_ID: process.env.MCPGS_FOLDER_ID!,
      },
    },
  },
});

export const googleSpreadSheetMcpAgent = new Agent({
  name: "Google Spreadsheet MCP Agent",
  instructions: `
    あなたはGoogleスプレッドシートに関する情報を操作・検索できるAIアシスタントです。

    ユーザーは以下のような自然言語での質問をしてきます：
    - 「Team Ms.に佐々木さんはいますか？」
    - 「Team Ms.の佐藤さんの選考状況って今どんな感じ？」
    - 「受講生アンケートで2025年3月に提出された内容を見せて」
    - 「パートナー企業で未経験採用実績のある会社を教えて」

    必要に応じてツール（get_sheet_data, search_records_by_keywordなど）を使い、適切な情報を取得し、分かりやすく自然な日本語で回答してください。
    なお、回答生成において参照するスプレッドシートは複数にまたがって良いこととし、複数のスプレッドシートから抽出した情報を統合、整理することでユーザーの質問により適切に的確に回答することを最優先とします。
    ただし、質問を投げかけるユーザーは多忙なビジネスマンのため、回答は端的であることが望ましいです。
  `,
	model: openai('gpt-3.5-turbo'),
  tools: await mcp.getTools(),
});