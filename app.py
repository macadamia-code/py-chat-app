from flask import Flask, request, jsonify, render_template, redirect
import psycopg2
import psycopg2.extras
from db import get_connection
from dotenv import load_dotenv
import os
from datetime import datetime

load_dotenv()

app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

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
