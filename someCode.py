import os
import subprocess
import hashlib
import requests
from flask import Flask, request



app = Flask(__name__)

# Hardcoded sensitive information (Issue 1)
API_KEY = "12345-secret-key"
DATABASE_PASSWORD = "password123"

@app.route('/command', methods=['GET'])
def run_command():
    # Command injection vulnerability (Issue 2)
    cmd = request.args.get('cmd')
    result = subprocess.check_output(cmd, shell=True)
    return f"Command output: {result}"

@app.route('/hash', methods=['POST'])
def hash_password():
    # Weak hashing algorithm (Issue 3)
    password = request.form.get('password')
    hashed_password = hashlib.md5(password.encode()).hexdigest()
    return f"Hashed password: {hashed_password}"

@app.route('/download', methods=['GET'])
def download_file():
    # Unvalidated URL for file download (Issue 4)
    file_url = request.args.get('url')
    response = requests.get(file_url)
    filename = os.path.basename(file_url)
    with open(filename, 'wb') as file:
        file.write(response.content)
    return f"File {filename} downloaded successfully!"

@app.route('/upload', methods=['POST'])
def upload_file():
    # Insecure file upload (Issue 5)
    file = request.files['file']
    upload_path = os.path.join("/uploads", file.filename)
    file.save(upload_path)
    return f"File uploaded to {upload_path}"

@app.route('/auth', methods=['POST'])
def authenticate():
    # Hardcoded credentials (Issue 6)
    username = request.form.get('username')
    password = request.form.get('password')
    if username == "admin" and password == "password123":
        return "Authenticated!"
    return "Invalid credentials", 401

if __name__ == '__main__':
    # Debug mode enabled (Issue 7)
    app.run(debug=True, host="0.0.0.0")