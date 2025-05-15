# ai-agent-google-spreadsheet

## .env
https://docs.google.com/document/d/1ZEQwFhDp4RcLVG1EPP9YaIX5THkGUQgHfm3Yg5SBgjg/edit?usp=sharing

## Slack 実験用ワークスペース参加URL
https://join.slack.com/t/ai-ctu2960/shared_invite/zt-35jd9j4tx-IXPOH6JQG1RdNlHPaabZJw

## 起動手順
### 1. 各ディレクトリに.envを作成し必要事項を記入
（上記リンク先に.envの内容を記載済み）
```bash
touch mcp-client/.env
touch mcp-server/.env
touch slack-bot/.env
```
### 2. Python仮想を有効化する
```bash
cd mcp-server
```
#### 仮想環境を作成
```bash
python3 -m venv .venv
```
#### 仮想環境を有効化（Mac/Linux）
```bash
source .venv/bin/activate
```
#### 仮想環境を有効化（Windows）
```bash
.venv\Scripts\activate
```

### 3. 必要なモジュールなどをインストール
```bash
pip install -r requirements.txt

cd ../mcp-client
npm install
```

### 4. mcp-clientを起動
```bash
npm run dev
```


### 5. Googleアカウントの認証を行う
ブラウザが自動で起動し、認証画面に遷移。
（もしうまくいかない場合はテストアカウントに追加する必要があるかもしれないので、めめまで語連絡ください。）

### 6. Mastraがhttp://localhost:4111で起動
この時点でmastraのUIでエージェントとの対話が可能。

### 7. slackを使用する場合
（必要に応じて別途ドキュメント作成します。）
諸設定完了後の起動
```bash
cd slack-bot
npx ts-node src/index.ts
```