from http.server import BaseHTTPRequestHandler
import json

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        
        response = json.dumps({
            "status": "success",
            "message": "🎉 LearnConnect API 部署成功！",
            "timestamp": "2024-01-15T10:00:00Z"
        })
        self.wfile.write(response.encode())
