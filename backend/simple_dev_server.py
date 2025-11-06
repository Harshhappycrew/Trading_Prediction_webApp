from http.server import BaseHTTPRequestHandler, HTTPServer
import json
from datetime import datetime

HOST = '0.0.0.0'
PORT = 8000

class Handler(BaseHTTPRequestHandler):
    def _send_json(self, data, status=200):
        payload = json.dumps(data).encode('utf-8')
        self.send_response(status)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Content-Length', str(len(payload)))
        self.end_headers()
        self.wfile.write(payload)

    def do_GET(self):
        if self.path == '/api/health' or self.path == '/api/health/':
            data = {
                "status": "healthy",
                "timestamp": datetime.utcnow().isoformat(),
                "service": "QuantEdge Trading Simulator"
            }
            self._send_json(data)
        elif self.path == '/api/status' or self.path == '/api/status/':
            data = {
                "api": "operational",
                "database": "connected",
                "ml_models": "not_loaded_in_fallback",
                "trading_engine": "inactive_in_fallback",
                "timestamp": datetime.utcnow().isoformat()
            }
            self._send_json(data)
        else:
            self.send_response(404)
            self.end_headers()

if __name__ == '__main__':
    server = HTTPServer((HOST, PORT), Handler)
    print(f"Simple dev server running at http://{HOST}:{PORT} (fallback)")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print('Shutting down')
        server.server_close()
