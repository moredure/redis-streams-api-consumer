from http.server import ThreadingHTTPServer


class Suicide:
    def __init__(self, server: ThreadingHTTPServer):
        self.server = server

    def die(self, signum: int, frame):
        self.server.shutdown()
