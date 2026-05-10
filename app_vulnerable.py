from flask import Flask, request
import sqlite3
import os

app = Flask(__name__)

# Setup a temporary in-memory database for demonstration
def init_db():
    conn = sqlite3.connect(':memory:', check_same_thread=False)
    conn.execute("CREATE TABLE users (id INTEGER PRIMARY KEY, username TEXT, password TEXT)")
    conn.execute("INSERT INTO users (username, password) VALUES ('admin', 'supersecret')")
    conn.commit()
    return conn

db_conn = init_db()

# Vulnerability 1: SQL Injection
# Accepts raw string formatting, allowing attackers to bypass authentication.
@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('username', '')
    password = request.form.get('password', '')
    
    # INTENTIONAL FLAW: String concatenation in SQL query
    query = f"SELECT * FROM users WHERE username='{username}' AND password='{password}'"
    cursor = db_conn.execute(query)
    user = cursor.fetchone()
    
    if user:
        return "Logged in successfully!", 200
    return "Invalid credentials", 401

# Vulnerability 2: Reflected Cross-Site Scripting (XSS)
# Directly renders user input into the HTML response without escaping.
@app.route('/greet', methods=['GET'])
def greet():
    name = request.args.get('name', 'Guest')
    # INTENTIONAL FLAW: Unescaped user input
    return f"<h1>Hello, {name}!</h1>", 200

# Vulnerability 3: Command Injection
# Uses user input directly in a system shell command.
@app.route('/ping', methods=['GET'])
def ping():
    ip = request.args.get('ip', '127.0.0.1')
    # INTENTIONAL FLAW: Executing arbitrary shell commands via input
    # e.g., passing "127.0.0.1; echo 'hacked'"
    result = os.popen(f"echo Pinging {ip}").read()
    return result, 200

if __name__ == '__main__':
    app.run(port=5000)