#!/usr/bin/env python3
import threading
import socket
import re
import os
import sys

porte = int(input())

def client():

    HOST = '172.26.30.59'  # The server's hostname or IP address
    PORT = 6254      # The port used by the server 
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(('', porte))
        s.connect((HOST, PORT))
        files = os.listdir()
        s.sendall('*'.join(files).encode())
        data = s.recv(1024)
        #print(data)
    sys.exit()


def server():

    HOST = '172.26.30.59'  # The server's hostname or IP address
    PORT = 6254      # The port used by the server
 
    
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind(('', porte+2))
        s.listen()
        
        while True:
            conn, addr = s.accept()
            print("connected")     # Establish connection with client.
            data = conn.recv(1024)
            filename=str(data)[2:-2]
            #print(str(data)[2:-2])
            f = open(filename,'rb')
            l = f.read(1024)
            while (l):
               conn.send(l)
               l = f.read(1024)
            f.close()

            print('Done sending the file')

            conn.close()

            print("enter 1 for client and 0 for server ")
   

def client_srch_retr():
    HOST = '172.26.30.59'  # The server's hostname or IP address
    PORT = 6254      # The port used by the server

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(('', porte+1))
        s.connect((HOST, PORT))
        
        fl = input("tell file name")

        s.sendall(b'search: ' + fl.encode())

        # print(fl)
        data = s.recv(1024)
        
    ip,port,file = str(data).split(':')
    ip = ip[2:]
    port = int(port)
    print(ip,port,file)
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(('', 2033))
        s.connect((ip,port))
        s.send(file.encode())
        with open(file, 'wb') as f:
            while True: 
                print('receiving data...')
                data = s.recv(1024)
                #print('data=%s', (data))
                if not data:
                    break
                f.write(data)
            print(str(file) + "recieved successfully")

    sys.exit()


    
if __name__ == "__main__":
    t2 = threading.Thread(target = server, name='t2')
    t2.start()
    while 1:
        t = int(input("enter 1 for client and 0 for server "))
        if t==1:
            t1 = threading.Thread(target = client_srch_retr, name='t1')
        else:
            t1 = threading.Thread(target = client, name='t1')

        t1.start()
        t1.join()
    t2.join()
