import os
import redis
from http.server import BaseHTTPRequestHandler, HTTPServer

cache = redis.Redis(host=os.getenv("REDIS_HOST", "redis"), port=6379)

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        print("Request for:", self.path, flush=True)
        if self.path != "/":
            self.send_response(404)
            self.end_headers()
            return
        visits = cache.incr("hits")
        message = f"Hello DevOps! This page was visited {visits} times.\n"
        self.send_response(200)
        self.send_header("Content-Type", "text/plain")
        self.end_headers()
        self.wfile.write(message.encode())

server = HTTPServer(("0.0.0.0", 5000), Handler)
print("Server running on port 5000...", flush=True)
server.serve_forever()
