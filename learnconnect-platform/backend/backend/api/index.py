from flask import Flask, jsonify
import os
import sys

# 添加路徑
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

try:
    from app import create_app
    app = create_app()
except Exception as e:
    app = Flask(__name__)
    
    @app.route('/')
    def home():
        return jsonify({"status": "success", "message": "LearnConnect API"})
    
    @app.route('/api/health')
    def health():
        return jsonify({"status": "healthy", "service": "LearnConnect"})

def handler(request, response):
    # 這是一個簡單的處理器，先用這個測試
    response.status_code = 200
    response.headers["Content-Type"] = "application/json"
    response.body = '{"status": "success", "message": "LearnConnect API is running"}'
    return response
