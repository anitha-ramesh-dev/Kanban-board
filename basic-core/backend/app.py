from http.server import BaseHTTPRequestHandler, HTTPServer
import json

class APIHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        if self.path == "/tasks":
            content_length = int(self.headers.get("Content-Length", 0))
            request_body = self.rfile.read(content_length)
            data = json.loads(request_body.decode("utf-8"))
            title = data.get("title")
            response = {
                "message": "Task created",
                "title": title
            }
            self.send_response(201)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps(response).encode())

server = HTTPServer(("localhost", 8000), APIHandler)

print("Server started on port 8000")

server.serve_forever()

