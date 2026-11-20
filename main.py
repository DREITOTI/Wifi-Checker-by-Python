import json
import threading
import webbrowser
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlparse

import speedtest


HOST = "127.0.0.1"
PORT = 8765
WEB_FILES = {
    "/": ("index.html", "text/html; charset=utf-8"),
    "/style.css": ("style.css", "text/css; charset=utf-8"),
    "/app.js": ("app.js", "text/javascript; charset=utf-8"),
}
state_lock = threading.Lock()
test_state = {
    "running": False,
    "status": "Ready to test your connection",
    "download": None,
    "upload": None,
    "ping": None,
    "error": None,
}


def json_response(handler, status, data):
    body = json.dumps(data).encode("utf-8")
    handler.send_response(status)
    handler.send_header("Content-Type", "application/json; charset=utf-8")
    handler.send_header("Content-Length", str(len(body)))
    handler.send_header("Cache-Control", "no-store")
    handler.end_headers()
    handler.wfile.write(body)


def update_state(**changes):
    with state_lock:
        test_state.update(changes)


def run_speed_test():
    try:
        update_state(status="Finding the best server...")
        wifi = speedtest.Speedtest()
        wifi.get_best_server()

        update_state(status="Measuring download speed...")
        download = wifi.download() / 1_000_000
        update_state(download=round(download, 2))

        update_state(status="Measuring upload speed...")
        upload = wifi.upload() / 1_000_000
        update_state(upload=round(upload, 2), ping=round(wifi.results.ping))

        update_state(running=False, status="Test complete")
    except Exception as exc:
        message = str(exc).strip() or exc.__class__.__name__
        update_state(running=False, status="Test failed", error=message)


class RequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        path = urlparse(self.path).path
        if path == "/api/status":
            with state_lock:
                data = dict(test_state)
            json_response(self, 200, data)
            return

        web_file = WEB_FILES.get(path)
        if web_file is None:
            self.send_error(404, "Not found")
            return

        filename, content_type = web_file
        body = (Path(__file__).parent / filename).read_bytes()
        self.send_response(200)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-cache")
        self.end_headers()
        self.wfile.write(body)

    def do_POST(self):
        if urlparse(self.path).path != "/api/test":
            self.send_error(404, "Not found")
            return

        with state_lock:
            if test_state["running"]:
                json_response(self, 409, {"error": "A test is already running"})
                return
            test_state.update(
                running=True,
                status="Starting speed test...",
                download=None,
                upload=None,
                ping=None,
                error=None,
            )

        threading.Thread(target=run_speed_test, daemon=True).start()
        json_response(self, 202, {"status": "started"})

    def log_message(self, format, *args):
        pass


def main():
    server = ThreadingHTTPServer((HOST, PORT), RequestHandler)
    url = f"http://{HOST}:{PORT}"
    print(f"Wi-Fi Speed Check is running at {url}")
    print("Press Ctrl+C to stop the server.")
    webbrowser.open_new_tab(url)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nStopping Wi-Fi Speed Check.")
    finally:
        server.server_close()


if __name__ == "__main__":
    main()
