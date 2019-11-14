# -*- coding: utf-8 -*-
#!/usr/bin/env python
"""
@author: Quentin
"""

import sys
import os
import subprocess

def PingIP(IP):

    output = subprocess.check_output("ping -c1 "+IP+"> /dev/null && echo 'Connected' || echo 'Disconnected'", shell=True)
    if("Connected" in output):
        return True
    else:
        return False

class NetWork:

    listeIP=[]

    def __init__(self):
        pass

    def addIP(self,IP):#Ajoute une IP à la liste
        self.listeIP.append([IP,0])

    def Scan(self):#Teste un PING unique pour chaque adresse
        for ip in range(0,len(self.listeIP)):
            IP=self.listeIP[ip][0]
            output = subprocess.check_output("ping -c1 "+IP+"> /dev/null && echo 'Connected' || echo 'Disconnected'", shell=True)
            if("Connected" in output):#Si l'IP répond, on réinitialise le nombre de "Non-Réponses"
                self.listeIP[ip][1]=0
            else:
                self.listeIP[ip][1]+=1#Sinon on incrémente

    def Disconnect(self,it=10):#On parcour la liste des Non-Réponse, et on peux spécifié la valeur max tolérée
        ListeDisconnected=[]
        for ip in range(0,len(self.listeIP)):
            if(self.listeIP[1]>=it):#Si la valeur max est atteinte
                ListeDisconnected.append(self.listeIP[ip])#On ajoute l'IP à la liste d'IP déconnectée qu'on fournira
        return ListeDisconnected
