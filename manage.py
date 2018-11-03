# import os
# import sys
# from server import Server
# # import socketserver  # In Python 2 use "import SocketServer" instead
# # from http import RequestHandler
# if __name__ == '__main__':
#     try:
#         # 
#         HOST, PORT = sys.argv[1].split(':')[0], int(sys.argv[1].split(':')[1])
#         print("Listening on http://%s:%d" % (HOST, PORT))
#         # socketserver.TCPServer((HOST, PORT), RequestHandler).serve_forever()
#         Server(HOST, PORT)
#     except Exception as e:
#         print(e)

#!/usr/bin/env python
import sys
import logging
import socket
import struct
import re
from util import *
from hashlib import sha1
from base64 import b64encode


logger = logging.getLogger()
clients = {}

def calculate_sec_websocket_accept(key):
    GUID = '258EAFA5-E914-47DA-95CA-C5AB0DC85B11'
    sha1_hash = sha1((key+GUID).encode())
    response_key = b64encode(sha1_hash.digest()).strip()
    return response_key.decode('ASCII')

def get_header(request):
    headers = request.decode().split("\r\n")
    if b"Connection: Upgrade" in request and b"Upgrade: websocket" in request:
        key = re.search(b'\n[sS]ec-[wW]eb[sS]ocket-[kK]ey[\s]*:[\s]*(.*)\r\n',request)
        if key:
            key = key.group(1)
        header = 'HTTP/1.1 101 Switching Protocols\r\n'\
                'Upgrade: websocket\r\n'              \
                'Connection: Upgrade\r\n'             \
                'Sec-WebSocket-Accept: %s\r\n'        \
                '\r\n' % calculate_sec_websocket_accept(key)
    else:
        msg = "Invalid Request"
        header = 'HTTP/1.1 200 OK\r\n'\
                'Connection: close\r\n'\
                'Content-Type: text/html; charset=UTF-8\r\n'\
                'Content-Length: %d\r\n'\
                'Access-Control-Allow-Origin: *\r\n\r\n'%len(msg)+msg
    return header.encode()

def main(host='0.0.0.0', port=5005):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((host, port))
    s.listen(1)
    s.settimeout(30)
    while True:
        try:
            conn, addr = s.accept()
            request_header = conn.recv(1024)
            print(request_header)
            # re.search()
            response_header = get_header(request_header)
            conn.send(response_header)
        except socket.timeout:
            continue

        logger.info('connection address: %s', addr)
        data = recv_msg(conn)
        priv_addr = msg_to_addr(data)
        send_msg(conn, addr_to_msg(addr))
        data = recv_msg(conn)
        data_addr = msg_to_addr(data)
        if data_addr == addr:
            logger.info('client reply matches')
            clients[addr] = Client(conn, addr, priv_addr)
        else:
            logger.info('client reply did not match')
            conn.close()

        logger.info('server - received data: %s', data)

        if len(clients) == 2:
            (addr1, c1), (addr2, c2) = clients.items()
            logger.info('server - send client info to: %s', c1.pub)
            send_msg(c1.conn, c2.peer_msg())
            logger.info('server - send client info to: %s', c2.pub)
            send_msg(c2.conn, c1.peer_msg())
            clients.pop(addr1)
            clients.pop(addr2)
    conn.close()

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')
    main(*addr_from_args(sys.argv))
