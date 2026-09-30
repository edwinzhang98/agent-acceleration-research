"""Serve only the generated report on an ephemeral loopback port."""
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path

REPORT = Path(__file__).resolve().parents[2] / 'notes/part3/2026-09-30-self-improvement-survey-mining-zh.html'

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path.split('?')[0] not in ('/', '/report.html'):
            self.send_error(404)
            return
        data = REPORT.read_bytes()
        self.send_response(200)
        self.send_header('Content-Type', 'text/html; charset=utf-8')
        self.send_header('Content-Length', str(len(data)))
        self.send_header('Cache-Control', 'no-store')
        self.end_headers()
        self.wfile.write(data)

    def log_message(self, *_):
        pass

if __name__ == '__main__':
    server = HTTPServer(('127.0.0.1', 0), Handler)
    print(f'http://127.0.0.1:{server.server_port}/report.html', flush=True)
    server.serve_forever()
