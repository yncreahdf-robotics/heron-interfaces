# -*- coding: utf-8 -*-
"""
Created on Tue Oct 15 14:11:40 2019

@author: Quentin
"""


# Import socket module 
import socket


import argparse
parser = argparse.ArgumentParser()
parser.add_argument("name")
args = parser.parse_args()
print(args.name)
  

def RecovPass():
    f= open("../Guess.txt","r")
    data=f.read()
    f.close()
    return(data)

def TakeName():
    pass



def Main():
    
    #name=TakeName()
    
    Server = '10.224.0.21'
    
    passwd=RecovPass()
  
    # Define the port on which you want to connect 
    port = 22322
  
    s = socket.socket(socket.AF_INET,socket.SOCK_STREAM) 
  
    # connect to server on local computer 
    s.connect((Server,port)) 
  
    # message you send to server 
    message = "Nyrio?"
     
  
    # message sent to server 
    s.send(message.encode('ascii')) 
  
    # messaga received from server 
    data = int(s.recv(1024).decode("ascii"))
    print(data)
    
    s.send(passwd[data:data+24].encode('ascii'))
    data2 = s.recv(1024).decode('ascii')
    print(data2)
  
        
    # close the connection 
    s.close() 
  
if __name__ == '__main__': 
    Main() 
