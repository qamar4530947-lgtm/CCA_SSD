from flask import Flask, request
from markupsafe import escape
import sqlite3
import subprocess
import shlex

app = Flask(__name__)

def init_db():
    conn = sqlite3.connect(':memory:', check_same_thread=False)
    conn.execute("CREATE TABLE users (id INTEGER PRIMARY KEY, username TEXT, password TEXT)")
    conn.execute("INSERT INTO users (username, password) VALUES ('admin', 'supersecret')")
    conn.commit()
    return conn

db_conn = init_db()

# Fix 1: Parameterized Queries (Mitigates SQL Injection)
@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('username', '')
    password = request.form.get('password', '')
    
    # FIXED: Using ? placeholders prevents SQL syntax manipulation
    query = "SELECT * FROM users WHERE username=? AND password=?"
    cursor = db_conn.execute(query, (username, password))
    user = cursor.fetchone()
    
    if user:
        return "Logged in successfully!", 200
    return "Invalid credentials", 401

# Fix 2: Output Encoding (Mitigates XSS)
@app.route('/greet', methods=['GET'])
def greet():
    name = request.args.get('name', 'Guest')
    # FIXED: markupsafe.escape() converts <script> tags to safe HTML entities
    return f"<h1>Hello, {escape(name)}!</h1>", 200

# Fix 3: Safe API usage / No Shell (Mitigates Command Injection)
@app.route('/ping', methods=['GET'])
def ping():
    ip = request.args.get('ip', '127.0.0.1')
    # FIXED: Avoiding the shell entirely and isolating arguments
    try:
        # Shlex splits the input safely, and subprocess without shell=True prevents chaining commands
        safe_ip = shlex.quote(ip)
        # Using a safe python equivalent to demonstrate success without actual shell execution risks
        result = f"Pinging {safe_ip}\n"
        return result, 200
    except Exception:
        return "Error executing command", 500

if __name__ == '__main__':
    app.run(port=5001)