from wshttp import WebsocketHttpServer
import json
class Server:
    clients = {}

    def client_left(self,client, server):
        try:
            self.clients.pop(client['id'])
        except:
            pass

    def new_client(self,client, server):
        print(client['address'])
        self.clients[client['id']] = client


    def msg_received(self,client, server, msg):
        if 1 in self.clients and msg == 'Connected':
            server.send_message(self.clients[1], "{:s}:{:d}".format(*client['address']))
            server.send_message(client, "{:s}:{:d}".format(*self.clients[1]['address']))
        else:
            pass #TODO Hosted client not found                

    def __init__(self,ip,port):
        server = WebsocketHttpServer(port, ip)
        server.set_fn_client_left(self.client_left)
        server.set_fn_new_client(self.new_client)
        server.set_fn_message_received(self.msg_received)
        server.run_forever()

