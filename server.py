# -*- coding: utf-8 -*-
"""
Spyder Editor

Editor : Quentin
"""


# import socket programming library
import socket
import SQLTools

# import thread module
from _thread import *
import threading
import random

print_lock = threading.Lock()

import mysql.connector




def RecovPass():
    f= open("../Guess.txt","r")
    data=f.read()
    f.close()
    return(data)


# thread fuction
def InitConnection(c,addr,passwd):
    while True:


            print(addr)
            start=random.randint(0,len(passwd)-100)
            # data received from client
            data = c.recv(1024)
            if not data:
                print('Bye')

                # lock released on exit
                print_lock.release()
                break

            # reverse the given string from client
            nameasked=data.decode('ascii')

            # send back reversed string to client
            c.send(str(start).encode('ascii'))
            data2=c.recv(1024).decode("ascii")
            print(data2)
            if(data2==passwd[start:start+24]):
                print("yes")
                resp=SQLTools.InsertID(nameasked)
                SQLTools.InsertCOMMANDS(resp,"DICTIONNARY","10.224.0.52")
                c.send("resp".encode('ascii'))
            else:
                c.send("No!".encode('ascii'))

    c.close()


def Main():
    host = ""

    passwd=RecovPass()
    port = 22322
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((host, port))
    print("socket binded to port", port)
    s.listen(5)
    print("socket is listening")


    while True:

        # establish connection with client
        c, addr = s.accept()

        # lock acquired by client
        print_lock.acquire()
        print('Connected to :', addr[0], ':', addr[1])
        # Start a new thread and return its identifier
        start_new_thread(InitConnection, (c,addr,passwd))
    s.close()


if __name__ == '__main__':
    Main()
