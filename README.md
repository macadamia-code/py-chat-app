# 💬 シンプルなチャットアプリ（HTML 版 & JSON API 版）

- **(1) HTML テンプレート方式**：毎回サーバーが HTML を組み立てて返します。
- **(2) JSON API 方式**：初回に HTML を取得し、以降は JSON API でメッセージを送受信します。

---

# 🛠️ 技術仕様

Flask 3.1.0
python-dotenv 1.1.0
psycopg2-binary 2.9.10

---

# 📁 ディレクトリ構成

```
.
├── README.md            # プロジェクト説明ファイル
├── app.py               # メインのFlaskアプリケーション
├── db.py                # データベース接続と操作
├── static               # 静的ファイル格納ディレクトリ
│   ├── script.js        # JavaScriptプログラム
│   └── styles.css       # CSSスタイルシート
├── templates            # HTMLテンプレート格納ディレクトリ
│   └── index.html       # メインページのテンプレート
├── .env                 # 環境変数
├── init.sql             # DB環境構築のためのSQL
└── requirements.txt     # 要インストールのパッケージ一覧
```

---

# 🐘 PostgreSQL データベース

PostreSQL で以下のデータベースが作成されていること。

- データベース名：postgres
- ユーザー名：postgres
- パスワード：postgres
- ポート番号：5432

異なる場合は .env ファイルの DATABASE_URL を適宜変更する。

---

# 🚀 セットアップ

1. PostgreSQL で以下の SQL を発行する。

```sql
DROP TABLE IF EXISTS messages;

CREATE TABLE messages (
  id SERIAL PRIMARY KEY,
  username TEXT NOT NULL,
  content TEXT NOT NULL,
  created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);
```

2. プロジェクト用のフォルダを作成する。

```shell
mkdir chat-app
cd chat-app
```

3. チャットアプリを GitHub から取得する。

```shell
git clone https://github.com/kaswister0116/todo_app.git .
```

4. 必要なパッケージをインストールする。

```shell
# 仮想環境を作成
python -m venv venv

# 仮想環境を有効化
source venv/Scripts/activate

# pipのアップグレード
python.exe -m pip install --upgrade pip

# ライブラリインストール
pip install -r requirements.txt
```

5. チャットアプリを起動する。

```shell
python app.py
```

---

## 🌐 アクセス URL

| パス    | 機能                                    |
| ------- | --------------------------------------- |
| `/`     | HTML ベースのチャット（リロードで更新） |
| `/json` | JSON API ベースのチャット（非同期通信） |

---

## 🔧 API エンドポイント（JSON API 用）

| メソッド                   | パス                                                | 内容 |
| -------------------------- | --------------------------------------------------- | ---- |
| `POST /api/messages`       | メッセージ送信 + `after` 以降のメッセージを取得     |
| `POST /api/messages/fetch` | `after` 以降のメッセージを取得（JSON ボディで送信） |
