import socket
import time
class Server:
    def generate_headers(self, response_code):
        header = ''
        if response_code == 200:
            header += 'HTTP/1.1 200 OK\n'
        elif response_code == 404:
            header += 'HTTP/1.1 404 Not Found\n'

        time_now = time.strftime("%a, %d %b %Y %H:%M:%S", time.localtime())
        header += 'Date: {now}\n'.format(now=time_now)
        header += 'Server: Simple-Python-Server\n'
        # Signal that connection will be closed after completing the request
        header += 'Connection: close\n\n'
        return header

    def __init__(self, addr):
        self.clients = []
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # To bind socket on existing port
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind(addr)
        s.listen(2)
        while True:
            conn, addr = s.accept()
            conn.recv(1024)
            conn.send((self.generate_headers(200)+'Hi I am in Heroku').encode())
            conn.close()
            # self.clients.append((conn, addr))
            # print(addr)
            # if len(self.clients) == 2:
            #     # data = '<html>\n<head><script>\nwindow.location.assign("http://{:s}:{:d}");\n\n</script>\n</head>\n</html>\n'.format(*self.clients[0][1])
            #     data = '<html>\n<head>\n<title>P2PHTTP</title>\n</head>\n<body>\n<iframe style="top:0;left:0;width:100%;height:100%;position:absolute;border:none" src="http://{:s}:{:d}">\n</iframe>\n</body></html>'.format(
            #         *self.clients[0][1])
            #     # data = "<html><body><center><h1>Error 404: File not found</h1></center><p>Head back to <a href=''>dry land</a>.</p></body></html>"
            #     msg = self.clients[1][0].recv(1024).decode()
            #     if msg:
            #         if msg.split(' ')[1] == '/':
            #             self.clients[0][0].send(
            #                 ("{:s}:{:d}".format(self.clients[1][1][0], self.clients[1][1][1]+3)).encode())
            #     self.clients[1][0].send(
            #         (self.generate_headers(200)+data).encode())
            #     conn.close()
            #     self.clients.pop()
            #     print("Done")
