import socket
class P2PServer:
    class Client:
        def __init__(self, conn, private_addr, public_addr):
            self.conn = conn
            self.private_addr = private_addr
            self.public_addr = public_addr

        def addressToMessage(self, addr):
            return '{}:{}'.format(addr[0], str(addr[1])).encode()

        def sendTwoEndpoint(self):
            return self.addressToMessage(self.private_addr) + b'|' + self.addressToMessage(self.public_addr)

    def addressToMessage(self, addr):
        return '{}:{}'.format(addr[0], str(addr[1])).encode('utf-8')

    def messageToAddress(self, msg):
        ip, port = msg.decode('utf-8').strip().split(':')
        return (ip, int(port))

    def __init__(self,addr):
        self.clients = []
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind(addr)
        s.listen(5)
        while len(self.clients)<2:
            conn,addr = s.accept()
            print(addr)
            conn.send(self.addressToMessage(addr))
            msg = conn.recv(1024)
            if msg:
                client_private_address = self.messageToAddress(msg)
                self.clients.append(self.Client(conn,client_private_address,addr))

        self.clients[0].conn.send(self.clients[1].sendTwoEndpoint())
        self.clients[1].conn.send(self.clients[0].sendTwoEndpoint())
        
        del self.clients
        conn.close()
        print("Done")

# if __name__ == "__main__":
#     server = P2PServer(('192.168.137.1',8080))


        
        


