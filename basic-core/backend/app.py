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
            cur.close()

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

    def do_GET(self):
      if self.path == "/tasks":
        cur = conn.cursor()
        query = load_sql("get_tasks.sql")
        cur.execute(query)  

        rows = cur.fetchall()
        cur.close()

        tasks=[]

        for row in rows:
            tasks.append({
                "id": row[0],
                "title": row[1]
            })
        self.send_response(200)
        self.send_header("Content-Type","application/json")
        self.end_headers()
        self.wfile.write(
            json.dumps(tasks).encode()
        )
        
server = HTTPServer(("localhost", 8000), APIHandler)

print("Server started on port 8000")

server.serve_forever()

