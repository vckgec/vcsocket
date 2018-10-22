import socketserver  # In Python 2 use "import SocketServer" instead


class RequestHandler(socketserver.StreamRequestHandler):
    def handle(self):
        command = self.rfile.readline()[5:-11].decode('UTF-8')
        print(command)

        if command == 'sleep':
            self.respond('Going to sleep')
        elif command == 'wakeup':
            self.respond('Waking up')
        else:
            self.respond('Unknown command')

    def respond(self, body):
        headers = '\r\n'.join([
            'HTTP/1.1 200 OK',
            'Connection: close',
            'Content-Type: text/plain; charset=UTF-8',
            'Content-Length: %d' % len(body.encode('UTF-8')),
            'Access-Control-Allow-Origin: *'
        ])
        self.wfile.write((headers + '\r\n\r\n' + body).encode('UTF-8'))


# HOST, PORT = '0.0.0.0', 8000
# print("Listening on http://%s:%d" % (HOST, PORT))
# socketserver.TCPServer((HOST, PORT), RequestHandler).serve_forever()
