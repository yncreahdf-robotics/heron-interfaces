# -*- coding: utf-8 -*-
#!/usr/bin/env python
"""
@author: Quentin
"""

import socket
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("name")
args = parser.parse_args()
print(args.name)


def RecovPass():#Récupère la phrase de passe à l'intérieur du fichier et stock la chaîne de caractère dans une variable (retournée)
    f= open("../Guess.txt","r")
    data=f.read()
    f.close()
    return(data)

def Main():

    Server = '10.224.0.52' #IP du Server
    passwd=RecovPass() #Récupération de la Phrase de passe


    port = 22322
    s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)#Préparation de la socket
    s.connect((Server,port))#Connection

    message= (args.name)#nom demandé
    s.send(message.encode('ascii'))#On envoi la demande
    data = int(s.recv(1024).decode("ascii"))#On récupère le mot de passe demandé
    s.send(passwd[data:data+24].encode('ascii'))#Et on l'envoi

    data2 = s.recv(1024).decode('ascii')#On récupère le message confirmant l'autorisation de communication
    #print(data2)
    s.close()#Fermeture de la connection

if __name__ == '__main__':
    Main()
