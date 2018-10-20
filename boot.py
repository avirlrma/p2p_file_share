import globals
import threading
import socket

def boot_network():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((globals.HOST, globals.PORT))
        s.listen()
        while True:
            conn, addr = s.accept()
            with conn:
                while True:
                    data = conn.recv(1024)
                    if not data:
                        break
                    conn.sendall(data)

if __name__=="__main__":
    t1 = threading.Thread(target = boot_network)
    t1.start()
    print("hello world")
    t1.join()