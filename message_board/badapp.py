from flask import Flask, render_template, request, redirect, url_for
import sqlite3
import datetime

app = Flask(__name__)

# 設定資料庫檔案路徑
DATABASE = './messages.db'

# 建立資料庫表格
def init_db():
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS messages
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  name TEXT,
                  message TEXT,
                  ip_address TEXT)''')
    conn.commit()
    conn.close()

# 初始化資料庫
init_db()

# 寫入 log 檔案
def log_ip(ip):
    now = datetime.datetime.now()
    timestamp = now.strftime("%Y-%m-%d %H:%M:%S")
    log_string = f"{timestamp} - {ip}\n"
    with open("logs.txt", "a") as f:
        f.write(log_string)

# 處理留言板首頁的請求
@app.route('/')
def index():
    # 紀錄 IP log
    log_ip(request.remote_addr)

    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    c.execute("SELECT * FROM messages ORDER BY id DESC")
    messages = c.fetchall()
    conn.close()
    return render_template('index.html', messages=messages)

# 處理提交留言的請求
@app.route('/add_message', methods=['POST'])
def add_message():
    name = request.form['name']
    message = request.form['message']
    ip_address = request.remote_addr  # 獲取客戶端的IP地址

    # 紀錄 IP log
    log_ip(ip_address)

    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    c.execute("INSERT INTO messages (name, message, ip_address) VALUES (?, ?, ?)", (name, message, ip_address))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
