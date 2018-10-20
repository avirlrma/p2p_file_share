import socket 
import threading 
import time
  
def threaded(c): 
    time.sleep(5)

  
  
def Main(): 
    host = "" 
    port = 6254
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
    s.bind((host, port)) 
    s.listen(5) 
    print("socket is listening") 
  
    # a forever loop until client wants to exit 
    while True: 
        c, addr = s.accept()
        print('Connected to :', addr[0], ':', addr[1]) 
        t1 = threading.Thread(threaded, (c,))
        t1.start()
    s.close() 
  
  
if __name__ == '__main__': 
    Main() 