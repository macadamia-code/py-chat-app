from flask import Flask, request, jsonify, render_template
import psycopg2
import psycopg2.extras
from db import get_connection
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

# チャットページを取得する
@app.route('/', methods=['GET'])
def json_page():
    return render_template('json_chat.html')

# すべてのメッセージをJSON形式で返す
@app.route('/api/get_messages', methods=['GET'])
def get_messages():
    db_type = os.getenv("DB_TYPE")
    query = "SELECT * FROM messages"

    query += " ORDER BY created_at DESC"

    conn = get_connection()
    if db_type == "postgresql":
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    else:
        cur = conn.cursor(dictionary=True)
    cur.execute(query)
    messages = cur.fetchall()
    cur.close()
    conn.close()

    return jsonify([dict(row) for row in messages])

# 受け取ったJSON形式のメッセージをデータベースに登録し、すべてのメッセージをJSON形式で返す
@app.route('/api/send_message', methods=['POST'])
def send_message():
    data = request.get_json()
    username = data['username']
    content = data['content']

    conn = get_connection()
    cur = conn.cursor()
    cur.execute("INSERT INTO messages (username, content) VALUES (%s, %s)", (username, content))
    conn.commit()
    cur.close()
    conn.close()

    return get_messages()

if __name__ == '__main__':
    port = int(os.getenv('PORT', 3000))
    app.run(host='0.0.0.0', port=port, debug=True)
