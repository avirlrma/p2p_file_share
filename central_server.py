import socket
import threading
import re

class Peer:
    def __init__( self, maxpeers, serverport, myid=None, serverhost = None ):
        self.debug = 0

        self.maxpeers = int(maxpeers)
        self.serverport = int(serverport)

            # If not supplied, the host name/IP address will be determined
        # by attempting to connect to an Internet host like Google.
        if serverhost: self.serverhost = serverhost
        else: self.__initserverhost()

            # If not supplied, the peer id will be composed of the host address
            # and port number
        if myid: self.myid = myid
        else: self.myid = '%s:%d' % (self.serverhost, self.serverport)

            # list (dictionary/hash table) of known peers
        self.peers = {}  

            # used to stop the main loop
        self.shutdown = False  

        self.handlers = {}
        self.router = None
        # end constructor


class Client:
    def __init__(self,ip,port):
        self.ip = ip
        self.port = port
        self.files = []

class ThreadedServer(object):
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind((self.host, self.port))
        self.clients = []

    def listen(self):
        self.sock.listen(5)
        while True:
            client, address = self.sock.accept()
            client_obj =  Client(address[0],int(address[1])) # can be changed to * somehting
            client.settimeout(60)
            self.clients.append(client_obj)
            print("connected to"+(address))
            t = threading.Thread(target = self.listenToClient,args = (client,address,client_obj)).start()

    def listenToClient(self, client, address,client_obj):
        size = 1024
        while True:
            data = client.recv(size)
            if data:
                if b'search' in data:
                    flag = 0
                    search_file = re.findall('search:(.*)',str(data))
                    print(search_file)
                    for client_dt in self.clients:
                        for file_names in client_dt.files:
                            if search_file[0][1:-1] in str(file_names):
                                flag = 1
                                client.sendall((str(client_dt.ip) +":" +str(client_dt.port+2)+":"+str(file_names)).encode())
                                break
                    if flag==0:
                        client.sendall(b"file not found")
                else:    
                    client_obj.files.extend(str(data).split('*'))
                    client_obj.files[0] = client_obj.files[0][2:]
                    print(client_obj.files)
                    client.sendall(b"Got the files mate")
            else:
                break
                raise error('Client disconnected')                 


if __name__ == "__main__":
    ThreadedServer('',6254).listen()
