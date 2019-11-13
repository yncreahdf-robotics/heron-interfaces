# -*- coding: utf-8 -*-
#!/usr/bin/env python


import sys
import os
import subprocess

def PingIP(IP):

    output = subprocess.check_output("ping -c1 "+IP+"> /dev/null && echo 'Connected' || echo 'Disconnected'", shell=True)
    if("Connected" in output):
        return True
    else:
        return False

#listeIP=["127.0.0.1","10.224.0.51","10.224.0.52","8.8.8.8"]

#for IP in listeIP:
#    print(IP,PingIP(IP))

class NetWork:

    listeIP=[]

    def __init__(self):
        pass

    def addIP(self,IP):
        self.listeIP.append([IP,0])

    def Scan(self):
        for ip in range(0,len(self.listeIP)):
            IP=self.listeIP[ip][0]
            output = subprocess.check_output("ping -c1 "+IP+"> /dev/null && echo 'Connected' || echo 'Disconnected'", shell=True)
            if("Connected" in output):
                self.listeIP[ip][1]=0
            else:
                self.listeIP[ip][1]+=1

    def Disconnect(self,it=10):
        ListeDisconnected=[]
        for ip in range(0,len(self.listeIP)):
            if(self.listeIP[1]>=it):
                ListeDisconnected.append(self.listeIP[ip])
        return ListeDisconnected

listeIP=["10.224.0.50","10.224.0.51","10.224.0.52"]

net=NetWork()

for ip in listeIP:
    net.addIP(ip)

try:
    while True:
        net.Scan()
        print("------")
        for ip in net.Disconnect():
            print(ip)
except:
    pass
