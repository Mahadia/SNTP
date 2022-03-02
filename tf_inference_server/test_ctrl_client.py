#!/usr/bin/env python3

import socket
from threading import Thread

def client_thread(idx, port, msg):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(('localhost', port))
    print(s)
    s.sendall(msg)
    data = s.recv(1024)
    s.close()
    print("Thread {} Received: {}".format(idx, repr(data)))

if __name__=="__main__":
    nt = Thread(target=client_thread, args=(1, 9919, b"shutdown"))
    nt.start()
    nt.join()
