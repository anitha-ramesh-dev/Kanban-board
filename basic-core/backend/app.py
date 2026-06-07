from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import psycopg2
from helpers.load_sql import load_sql

conn = psycopg2.connect(
    host="localhost",
    database="kanban",
    user="anitha",
    password="postgres"
)

class APIHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        if self.path == "/tasks":
            # get payload and header
            content_length = int(self.headers.get("Content-Length", 0))
            request_body = self.rfile.read(content_length)
            data = json.loads(request_body.decode("utf-8"))
            title = data.get("title")

            # store in db
            cur = conn.cursor()

            query = load_sql("insert_task.sql")
            cur.execute(query, (title,))

            task_id = cur.fetchone()[0]
            conn.commit()
            conn.close()

            # send response
            response = {
                "id": task_id,
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

