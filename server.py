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
        data = '<html>\n<head>\n<title>P2PHTTP</title>\n</head>\n<body>\n<iframe style="top:0;left:0;width:100%;height:100%;position:absolute;border:none" src="http://{:s}:{:d}">\n</iframe>\n</body></html>'.format(*self.clients[1]['address'])
        if '/favicon.ico' not in msg:
            server.send_message(self.clients[1], "{:s}:{:d}".format(client['address'][0],client['address'][1]+1))
        server.respond(client,data)
                

    def __init__(self,ip,port):
        server = WebsocketHttpServer(port, ip)
        server.set_fn_client_left(self.client_left)
        server.set_fn_new_client(self.new_client)
        server.set_fn_message_received(self.msg_received)
        server.run_forever()

