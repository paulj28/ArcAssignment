import http.server
import socketserver
import json

port = 8000

Handler = http.server.SimpleHTTPRequestHandler

class Handler(http.server.SimpleHTTPRequestHandler):
    def noEndpoint(self):
        self.send_response(400)
        self.send_header("Content-type", "application/json")
        self.end_headers()
        self.wfile.write(bytes(json.dumps({'error':'Bad Endpoint'}), 'utf-8'))

    def do_GET(self):
        senddata={}
        with open('fav.json') as f:
            senddata=json.load(f) 
        self.send_response(200)
        self.send_header("Content-type", "application/json")
        self.end_headers()
        self.wfile.write(bytes(json.dumps(senddata), 'utf-8'))

    def do_POST(self):
        self.send_response(400)
        self.send_header("Content-type", "application/json")
        self.end_headers()
        self.wfile.write(bytes(json.dumps({'error': 'Invalid Request'}), 'utf-8'))

with socketserver.TCPServer(("", port), Handler) as httpd:
    print("serving at port", port)
    httpd.serve_forever()