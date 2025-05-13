# 各ファイルの役割
- `main.py` : エントリーポイント
- `config.py` : .env読み込み、設定管理（python-dotenv）
- `google_auth.py` : google-auth-oauthlibによる認証処理
- `google_drive` : Drive API操作（google-api-python-client）
- `google_sheet` : Sheets API操作（gspread or google-api-python-client）

# 必要なライブラリ
認証をブラウザで開かせる処理（Go版のOpening browser for authentication相当）も google-auth-oauthlib.flow.InstalledAppFlow で再現できます。
```bash
pip install google-auth google-auth-oauthlib google-auth-httplib2 google-api-python-client flask
```

# 仮想環境
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

#### 仮想環境を終了
```bash
deactivate
```

# パッケージ
#### パッケージをインストール
```bash
pip install パッケージ名
```

#### 複数パッケージを一括インストール
```bash
pip install -r requirements.txt
```

#### 現在の環境の依存関係をファイルに書き出す
```bash
pip freeze > requirements.txt
```

# .env
```txt
必要事項を随時追記
```
## エラー対処
```bash
ModuleNotFoundError: No module named 'mcp'
```
が出たら...@mastra/mcp に対応する Python側の mcp パッケージ（Model Context Protocol） がインストールされていないことを示しているので
```bash
pip install modelcontextprotocol
```
を実行すればOK。

## 手順：mcp-google-spreadsheet を zsh で使えるようにする
① .zshrc を開く
```bash
nano ~/.zshrc
```
② 最後にこの1行を追加：
```bash
alias mcp-google-spreadsheet='/Users/uchihifamily/mcp-google-spreadsheet/mcp-server-spreadsheet-Python/.venv/bin/python /Users/uchihifamily/mcp-google-spreadsheet/mcp-server-spreadsheet-Python/main.py'
```

③ 保存して終了（nanoの場合）
	•	Ctrl + O → Enter（保存）
	•	Ctrl + X（終了）

④ 反映させる
```bash
source ~/.zshrc
```

⑤ 動作確認
```bash
mcp-google-spreadsheet
```


クライアントに実行ファイルの実行権限を与える
```bash
chmod +x /Users/uchihifamily/mcp-google-spreadsheet/mcp-server-spreadsheet-Python/mcp-google-spreadsheet
```
