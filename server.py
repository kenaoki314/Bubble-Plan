"""Serves the task map and syncs its state between machines.

Static files (index.html etc.) are served as usual; the board state lives in
state.json next to this file and is exposed at /state:

  GET /state  -> the saved {rev, state} JSON, or `null` if nothing saved yet
  PUT /state  -> replace the saved JSON (validated, written atomically)

Run it on ONE machine (e.g. the desktop):  python server.py
Then open the map from any device on the same network with
http://<that-machine's-ip>:8127 - every device sees and edits the same map.
"""
import json
import os
from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler

ROOT = os.path.dirname(os.path.abspath(__file__))
STATE_FILE = os.path.join(ROOT, "state.json")
PORT = 8127


class Handler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=ROOT, **kwargs)

    def _path(self):
        return self.path.split("?", 1)[0]

    def do_GET(self):
        if self._path() == "/state":
            body = b"null"
            if os.path.exists(STATE_FILE):
                with open(STATE_FILE, "rb") as f:
                    body = f.read()
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Cache-Control", "no-store")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)
            return
        super().do_GET()

    def do_PUT(self):
        if self._path() != "/state":
            self.send_response(404)
            self.end_headers()
            return
        length = int(self.headers.get("Content-Length") or 0)
        body = self.rfile.read(length)
        try:
            json.loads(body)
        except ValueError:
            self.send_response(400)
            self.end_headers()
            return
        tmp = STATE_FILE + ".tmp"
        with open(tmp, "wb") as f:
            f.write(body)
        os.replace(tmp, STATE_FILE)  # atomic: readers never see a half-written file
        self.send_response(204)
        self.end_headers()

    def log_message(self, *args):
        pass  # keep the console quiet


if __name__ == "__main__":
    print(f"task map on http://localhost:{PORT}  (state file: {STATE_FILE})")
    print("open from another device via this machine's LAN IP, e.g. http://192.168.x.x:8127")
    ThreadingHTTPServer(("0.0.0.0", PORT), Handler).serve_forever()
