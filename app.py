from flask import Flask, request, jsonify, render_template, redirect
from db import get_connection
from dotenv import load_dotenv
import os
import psycopg2.extras
from flasgger import Swagger
from datetime import datetime

load_dotenv()

app = Flask(__name__)
swagger = Swagger(app)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

# 静的ファイルとテンプレートの設定はデフォルトのままでOK

@app.route('/')
def index():
    conn = get_connection()
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cur.execute("SELECT * FROM messages ORDER BY created_at DESC")
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return render_template('index.html', messages=rows)

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

@app.route('/json')
def json_page():
    return render_template('json.html')

@app.route('/api/get_messages')
def get_messages():
    """
    メッセージの取得
    ---
    parameters:
      - name: after
        in: query
        type: string
        format: date-time
        required: false
        description: この日時以降のメッセージを取得
    responses:
      200:
        description: メッセージ一覧の取得成功
        schema:
          type: array
          items:
            $ref: '#/definitions/Message'
    """
    after = request.args.get('after')
    query = "SELECT * FROM messages"
    params = []

    if after:
        query += " WHERE created_at > (%s AT TIME ZONE 'Asia/Tokyo')"
        params.append(after)

    query += " ORDER BY created_at DESC"

    conn = get_connection()
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cur.execute(query, params)
    messages = cur.fetchall()
    cur.close()
    conn.close()

    return jsonify([dict(row) for row in messages])

@app.route('/api/send_message', methods=['POST'])
def send_message():
    """
    メッセージの投稿
    ---
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          properties:
            username:
              type: string
            content:
              type: string
            after:
              type: string
              format: date-time
    responses:
      201:
        description: 新着メッセージの配列
        schema:
          type: array
          items:
            $ref: '#/definitions/Message'
    """
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

@app.route('/sample')
def sample_page():
    return app.send_static_file('sample.html')

if __name__ == '__main__':
    port = int(os.getenv('PORT', 3000))
    app.run(host='0.0.0.0', port=port, debug=True)

swagger.template['definitions'] = {
    'Message': {
        'type': 'object',
        'properties': {
            'id': {
                'type': 'integer',
                'example': 1
            },
            'username': {
                'type': 'string',
                'example': 'Taro'
            },
            'content': {
                'type': 'string',
                'example': 'こんにちは'
            },
            'created_at': {
                'type': 'string',
                'format': 'date-time',
                'example': '2024-05-15T11:00:00Z'
            }
        }
    }
}