import os
import sys
from server import Server
# import socketserver  # In Python 2 use "import SocketServer" instead
# from http import RequestHandler
if __name__ == '__main__':
    try:
        # 
        HOST, PORT = sys.argv[1].split(':')[0], int(sys.argv[1].split(':')[1])
        print("Listening on http://%s:%d" % (HOST, PORT))
        # socketserver.TCPServer((HOST, PORT), RequestHandler).serve_forever()
        Server(HOST, PORT)
    except Exception as e:
        print(e)
