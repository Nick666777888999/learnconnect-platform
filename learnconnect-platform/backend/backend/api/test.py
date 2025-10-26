from http.server import BaseHTTPRequestHandler
import json

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        
        response = json.dumps({
            'status': 'success',
            'message': 'LearnConnect API is working!',
            'endpoints': {
                '/api/auth/login': 'POST - User login',
                '/api/auth/register': 'POST - User registration',
                '/api/chat/rooms': 'GET - Get chat rooms',
                '/api/stats': 'GET - Platform statistics'
            }
        })
        self.wfile.write(response.encode())

def handler(request, response):
    h = Handler(request, response, {})
    h.do_GET()
    return response
