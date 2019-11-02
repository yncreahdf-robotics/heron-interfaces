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
def threaded(c,addr,passwd):
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
                c.send("resp".encode('ascii'))
            else:
                c.send("No!".encode('ascii'))
            
        
        
  
    # connection closed 
    c.close() 
  
  
def Main(): 
    host = ""
    
    passwd=RecovPass()
    #start=random.randint(0,len(passwd)-100)
    # reverse a port on your computer 
    # in our case it is 12345 but it 
    # can be anything 
    port = 22322
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
    s.bind((host, port)) 
    print("socket binded to port", port) 
  
    # put the socket into listening mode 
    s.listen(5) 
    print("socket is listening") 
  
    # a forever loop until client wants to exit 
    while True: 
  
        # establish connection with client 
        c, addr = s.accept() 
  
        # lock acquired by client 
        print_lock.acquire() 
        print('Connected to :', addr[0], ':', addr[1])  
        # Start a new thread and return its identifier 
        start_new_thread(threaded, (c,addr,passwd)) 
    s.close() 
  
  
if __name__ == '__main__': 
    Main() 
