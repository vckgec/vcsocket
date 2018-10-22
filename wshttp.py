from websocket_server import WebSocketHandler
from http_server import BaseHTTPRequestHandler
class WSHTTPHandler(WebSocketHandler,BaseHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        print(self.rfile.readline(1))