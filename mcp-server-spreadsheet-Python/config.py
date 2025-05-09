# .env読み込み、設定管理（python-dotenv）

from dotenv import load_dotenv
import os

load_dotenv()

CLIENT_SECRET_PATH = os.getenv("CLIENT_SECRET_PATH", "client_secret.json")
TOKEN_PATH = os.getenv("TOKEN_PATH", "token.json")