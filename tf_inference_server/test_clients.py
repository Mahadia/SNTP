#!/usr/bin/env python3

import socket
from threading import Thread

def client_thread(idx, msg):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(('localhost', 9909))
    print(s)
    s.sendall(msg)
    data = s.recv(1024)
    s.close()
    print("Thread {} Received: {}".format(idx, repr(data)))

if __name__=="__main__":
    texts = [b"I hate it",
            b"I love it",
            b"its okay i guess",
            b"Absolutely wonderful",
            b"A complete waste of time",
            b"I've never been so embarassed",
            b"It was a wonderful experience",
            b"A for effort, F for execution",
            b"yum yum tasty"]

    for i in range(0,len(texts)):
        nt = Thread(target=client_thread, args=(i, texts[i]))
        nt.start()
        nt.join()
