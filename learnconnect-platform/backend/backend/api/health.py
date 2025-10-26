from http.server import BaseHTTPRequestHandler
import json

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        
        response = json.dumps({
            "status": "success",
            "service": "LearnConnect Backend",
            "version": "1.0.0",
            "endpoints": [
                "/api/health",
                "/api/auth/login", 
                "/api/auth/register",
                "/api/chat/rooms",
                "/api/stats"
            ]
        })
        self.wfile.write(response.encode())
