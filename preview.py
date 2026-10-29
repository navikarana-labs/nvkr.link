"""Local static 404 preview; Apache .htaccess redirects are not emulated."""

from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path


class PreviewHandler(SimpleHTTPRequestHandler):
    def list_directory(self, path):
        self.send_error(404)
        return None

    def send_error(self, code, message=None, explain=None):
        if code != 404:
            return super().send_error(code, message, explain)

        try:
            body = (Path(self.directory) / "404.html").read_bytes()
        except OSError:
            return super().send_error(code, message, explain)

        self.send_response(404)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        if self.command != "HEAD":
            self.wfile.write(body)


if __name__ == "__main__":
    handler = partial(PreviewHandler, directory=str(
        Path(__file__).resolve().parent))
    with ThreadingHTTPServer(("127.0.0.1", 8000), handler) as server:
        print("Static 404 preview: http://localhost:8000/404.html (Ctrl+C to stop)")
        try:
            server.serve_forever()
        except KeyboardInterrupt:
            pass
