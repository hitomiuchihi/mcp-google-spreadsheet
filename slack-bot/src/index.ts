import { App, ExpressReceiver } from "@slack/bolt";
import axios from "axios";
import * as dotenv from "dotenv";

dotenv.config();

// ✅ ExpressReceiverを使って /slack/events を公開
const receiver = new ExpressReceiver({
  signingSecret: process.env.SLACK_SIGNING_SECRET!,
  endpoints: "/slack/events", // これがSlackの検証先
});

const baseUrl = process.env.MCP_CLIENT_URL;

const app = new App({
  token: process.env.SLACK_BOT_TOKEN!,
  receiver, // Slack Events を受け取る
});

// ✅ メッセージイベントの処理
app.message(async ({ message, say }) => {
  if (!("text" in message)) return;

  const userMessage = message.text;
  console.log("📥 Slackからのメッセージ:", userMessage);

  try {
    console.log("📤 Mastraに送るリクエスト:");
    console.log({
      messages: [{ role: "user", content: userMessage }]
    });

    const response = await axios.post(`${baseUrl}/api/agents/googleSpreadSheetMcpAgent/generate`, {
      messages: [{ role: "user", content: userMessage }]
    });

    console.log("📥 Mastraからのレスポンス:", response.data.text);

    const reply = response.data.text || "すみません、うまく返答できませんでした";
    await say(reply);
  } catch (error: any) {
    console.error("❌ Mastraエージェントとの通信に失敗:", error.message);
    if (error.response) {
      console.error("❗ status:", error.response.status);
      console.error("❗ body:", error.response.data);
    }
    await say("エージェントとの通信でエラーが発生しました。");
  }
});

// ✅ サーバー起動
(async () => {
  const port = 3000;
  await app.start(port);
  console.log(`⚡️ Slack bot is running on http://localhost:${port}`);
})();
