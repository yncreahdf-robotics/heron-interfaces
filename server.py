# -*- coding: utf-8 -*-
"""
Editor : Quentin
"""

import socket
import SQLTools
from _thread import *
import threading
import random

print_lock = threading.Lock()

import mysql.connector

def RecovPass():#Récupère la phrase de passe
    f= open("../Guess.txt","r")
    data=f.read()
    f.close()
    return(data)


# thread fuction
def InitConnection(c,addr,passwd):
    while True:
            start=random.randint(0,len(passwd)-100)#On choisi le mot de passe
            # data received from client
            data = c.recv(1024)#On reçoit l'ID demandé
            if not data:#Si l'ID est vide
                print('Bye')
                # lock released on exit
                print_lock.release()
                break

            nameasked=data.decode('ascii')
            data2=c.recv(1024).decode("ascii")

            print(data2)
            if(data2==passwd[start:start+24]):
                print("yes")
                resp=SQLTools.InsertID(nameasked)
                SQLTools.InsertCOMMANDS("Init-Central/"+resp,resp,"DICTIONNARY","10.224.0.52")
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
        c, addr = s.accept()
        # lock acquired by client
        print_lock.acquire()
        print('Connected to :', addr[0], ':', addr[1]) #On affiche l'IP du client
        # Start a new thread and return its identifier
        start_new_thread(InitConnection, (c,addr,passwd))


if __name__ == '__main__':
    Main()
