from http.server import BaseHTTPRequestHandler, HTTPServer
from threading import Thread, Event
import json

RUN_EVENT = Event()
STOP_EVENT = Event()
STOP_EVENT.set()

class ControlHandler(BaseHTTPRequestHandler):
    def send_json(self, data):
        body = json.dumps(data).encode()
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        if self.path == "/status":
            self.send_json({"running": RUN_EVENT.is_set()})
        else:
            self.send_error(404)

    def do_POST(self):
        if self.path == "/start":
            STOP_EVENT.clear()
            RUN_EVENT.set()
            self.send_json({"ok": True, "running": True})
        elif self.path == "/stop":
            RUN_EVENT.clear()
            STOP_EVENT.set()
            self.send_json({"ok": True, "running": False})
        else:
            self.send_error(404)

    def log_message(self, *args):
        pass

def start_server():
    server = HTTPServer(("127.0.0.1", 8765), ControlHandler)
    Thread(target=server.serve_forever, daemon=True).start()
    print("Control server ready: 127.0.0.1:8765")
