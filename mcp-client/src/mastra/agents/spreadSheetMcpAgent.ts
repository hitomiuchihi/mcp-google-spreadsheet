import { openai } from "@ai-sdk/openai"; // OpenAI SDKをインポート
import { Agent } from "@mastra/core/agent";
import { MCPClient } from "@mastra/mcp";
import { accessible_spreadsheets } from "../accesible_sheets";

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

try {
  const tools = await mcp.getTools();
  // console.log("✅ tools:", JSON.stringify(tools, null, 2));
  console.log("✅ Registered tools:", Object.keys(tools));
  // console.log("🛠️ Sample get_sheet_data:", tools);
} catch (err) {
  console.error("❌ MCP getTools failed:", err);
}

export const googleSpreadSheetMcpAgent = new Agent({
  name: "Google Spreadsheet MCP Agent",
  instructions: `
    あなたはGoogleスプレッドシートに関する情報を操作・検索できるAIアシスタントです。

    以下のツールを使ってユーザーの質問に答えてください：

  - **mcp_google_spreadsheet_get_sheet_data**  
    指定したスプレッドシートとシートのデータを取得します。  
    引数: \`spreadsheet_name\`, \`sheet_name\`, \`range_\`

  - **mcp_google_spreadsheet_get_all_sheets_data**  
    指定したスプレッドシート内のすべてのシートのデータを取得します。  
    引数: \`spreadsheet_name\`

  - **mcp_google_spreadsheet_search_records_by_keyword**  
    指定したスプレッドシートの中からキーワードに一致する行を検索します。  
    引数: \`spreadsheet_name\`, \`keyword\`


    スプレッドシートについては以下のものにアクセスすることができ、それぞれスプレッドシートの役割も以下の通りです。
    ・「受講生選考状況」
      説明：自社のプログラミングスクール受講生の転職活動における選考状況を管理するためのスプレッドシート
      URL：https://docs.google.com/spreadsheets/d/1LB3QS6peeSwadoguqhuFNfE53euEyQt--mHDoO9b8SY/edit?usp=sharing
    ・「Team Ms.メンバー」
      説明：自社プログラミングスクールの卒業生でパートナー企業に派遣されている/される可能性のあるTeam Ms.という組織のメンバー情報を管理するためのスプレッドシート
      URL: https://docs.google.com/spreadsheets/d/1a8mEaBSPvrGq6lZnrreAIgfmWDDhBtZeAvsOFa2Lu1c/edit?usp=sharing
    ・「パートナー企業」
      説明：Team Ms.のメンバーがインターンや業務委託という形態で派遣される可能性のある企業の情報を管理するためのスプレッドシート
      URL：https://docs.google.com/spreadsheets/d/1DHXzO8mUFYX6oMlrVzN6UOFEyxtG-qV27wGPd8rFYcA/edit?usp=sharing
    ・「受講生アンケート」
      説明：自社プログラミングスクールで現在受講中の受講生がm回収提出するアンケート結果を蓄積、管理しているスプレッドシート
      URL：https://docs.google.com/spreadsheets/d/1KKUJ8xcVGXevSEM9AnRKAifjZ1_xJsVU487fC6BPu-s/edit?usp=sharing

    ユーザーは以下のような自然言語での質問をしてきます：
    - 「Team Ms.に佐々木さんはいますか？」
    - 「Team Ms.の佐藤さんの選考状況って今どんな感じ？」
    - 「受講生アンケートで2025年3月に提出された内容を見せて」
    - 「パートナー企業で未経験採用実績のある会社を教えて」

    アクセス可能なスプレッドシートから、能動的に判断して適切な情報を取得し、分かりやすく自然な日本語で回答してください。
    なお、回答生成において参照するスプレッドシートは複数にまたがって良いこととし、複数のスプレッドシートから抽出した情報を統合、整理することでユーザーの質問により適切に的確に回答することを最優先とします。
    ただし、質問を投げかけるユーザーは多忙なビジネスマンのため、回答は端的であることが望ましいです。

    なお、スプレッドシートを参照するためにMCPサーバーのツールを利用すると思いますが、ツールには
    プレフィックスとして mcp_google_spreadsheet_ をつけて呼び出すようにしてください。
  `,
	model: openai('gpt-4o'),
  tools: await mcp.getTools(),
});
