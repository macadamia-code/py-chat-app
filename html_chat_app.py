from flask import Flask, request, render_template, redirect
import psycopg2
import psycopg2.extras
from db import get_connection
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

# すべてのメッセージを記載したHTMLファイルを返す
@app.route('/', methods=['GET'])
def index():
    db_type = os.getenv("DB_TYPE")
    conn = get_connection()

    if db_type == "postgresql":
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    else:
        cur = conn.cursor(dictionary=True)

    cur.execute("SELECT * FROM messages ORDER BY created_at DESC")
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return render_template('html_chat.html', messages=rows)

# 受け取ったメッセージをデータベースに登録し、すべてのメッセージを記載したHTMLファイルを返す
@app.route('/', methods=['POST'])
def post_message():
    username = request.form['username']
    content = request.form['content']
    if username and content:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("INSERT INTO messages (username, content) VALUES (%s, %s)", (username, content))
        conn.commit()
        cur.close()
        conn.close()
    return redirect('/')

if __name__ == '__main__':
    port = int(os.getenv('PORT', 3000))
    app.run(host='0.0.0.0', port=port, debug=True)
