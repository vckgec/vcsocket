from websocket_server import WebsocketServer
import json
class Server:
    clients = {}

    def client_left(self,client, server):
        try:
            self.clients.pop(client['id'])
        except:
            pass

    def new_client(self,client, server):
        self.clients[client['id']] = client


    def msg_received(self,client, server, msg):
        if client['id']==1:
            message = json.loads(msg)
            server.send_message(self.clients[int(message['id'])], json.dumps(message['message']))
        else:
            server.send_message(self.clients[1],json.dumps({'id':client['id'],'message':msg}))

    def __init__(self,ip,port):
        server = WebsocketServer(port,ip)
        server.set_fn_client_left(self.client_left)
        server.set_fn_new_client(self.new_client)
        server.set_fn_message_received(self.msg_received)
        server.run_forever()

