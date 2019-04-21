from http.server import BaseHTTPRequestHandler
from urllib.parse import parse_qs, urlparse
from src.components.ad_events_consumer import AdEventsController


class Listener(BaseHTTPRequestHandler):
    def __init__(self, controller: AdEventsController, *args):
        self.controller = controller
        super().__init__(*args)

    def do_POST(self):
        query_components = parse_qs(urlparse(self.path).query)
        self.controller.process_ad_event(query_components)
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        self.wfile.write('OK')
