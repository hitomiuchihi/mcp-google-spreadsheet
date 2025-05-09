import { openai } from "@ai-sdk/openai"; // OpenAI SDKをインポート
import { Agent } from "@mastra/core/agent";
// import { MCPConfiguration } from "@mastra/mcp"; // MCPConfigurationは非推奨→代わりにMCPClient
import { MCPClient } from "@mastra/mcp";

// BraveのAPi Keyがない時にアラートを出す場合は以下を使用
// if (!process.env.BRAVE_API_KEY) {
//   throw new Error("BRAVE_API_KEY is not defined in environment variables");
// }

// MCP定義
// const mcp = new MCPConfiguration({   MCPConfigurationは非推奨になったのでMCPClientを使用
const mcp = new MCPClient({
	// MCPサーバー情報
  servers: {
    // stdio example
    "github": {
      "command": "npx",
      "args": [
        "-y",
        "@modelcontextprotocol/server-brave-search"
      ],
      env: {
        "BRAVE_API_KEY": process.env.BRAVE_API_KEY ?? "", //  ?? "" を削除したい場合は line 7-9 を有効にする
      },
    },
  },
});

export const sampleMcpAgent = new Agent({
  name: "Sample MCP Agent",
  instructions: `
      あなたはウェブ検索ができる便利なアシスタントです。

      【情報を求められた場合】
      webSearchToolを使用してウェブ検索を実行してください。webSearchToolは以下のパラメータを受け付けます：
      - query: 検索クエリ（必須）
      - country: 検索結果の国コード（例: JP, US）（オプション）
      - count: 返される検索結果の最大数（オプション）
      - search_lang: 検索言語（例: ja, en）（オプション）

      回答は常に簡潔ですが情報量を保つようにしてください。ユーザーの質問に直接関連する情報を優先して提供してください。
  `,
  // model: anthropic("claude-3-5-sonnet-20241022"), // openai('gpt-4o'),に変更したい
	model: openai('gpt-4o'),
  tools: await mcp.getTools(),
});