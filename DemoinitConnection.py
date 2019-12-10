# -*- coding: utf-8 -*-
#!/usr/bin/env python
"""
@author: Quentin
"""

import socket
import SQLTools
import SELECTTools
import InsertTools
import time
import subprocess
import PubForHeron

import rospy
from std_msgs.msg import String


ListFunction=[['DICTIONNARY','DICTIONNARY',''],
['TEMPERATURE','TEMPERATURE(nZone)','Return in Comm the TEMPERATURE of the zone : BCPU-therm / MCPU-therm / GPU-therm / PLL-therm / Tboard_tegra / Tdiode_tegra / PMIC-Die / thermal-fan-est'],
['CIRCLE','CIRCLE','']]

def RecovPass():#Récupère la phrase de passe à l'intérieur du fichier et stock la chaîne de caractère dans une variable (retournée)
    f= open("../Guess.txt","r")
    data=f.read()
    f.close()
    return(data)

def InitConnection(name):

    Server = '10.224.0.52' #IP du Server
    passwd=RecovPass() #Récupération de la Phrase de passe


    port = 22322
    s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)#Préparation de la socket
    s.connect((Server,port))#Connection

    s.send(name.encode('ascii'))#On envoi la demande
    data = int(s.recv(1024).decode("ascii"))#On récupère le mot de passe demandé
    s.send(passwd[data:data+24].encode('ascii'))#Et on l'envoi

    data2 = s.recv(1024).decode('ascii')#On récupère le message confirmant l'autorisation de communication
    #print(data2)
    s.close()#Fermeture de la connection
    return data2

ID=InitConnection("heron")

print("----------------------")

#InsertTools.InsertCOMMANDS('fortheTest',ID,'TEMPERATURE(4)','fortheTest',com=None)

now=time.time()
while(time.time()-now<1000):
    #print(time.time()-now)
    commands=SELECTTools.CommandsFor(ID)
    for elt in commands:
        LineOrder,OrderID,Function,Target,Status,Source,ComOrder=elt[0],elt[1],elt[2],elt[3],elt[4],elt[5],elt[6]
        if(Status=='waiting'):
                if(Status=='waiting'):

                    if(Function=='DICTIONNARY'):
                        print("DICTIONNARY")
                        #time.sleep(5)
                        InsertTools.ChangeCOMMANDS("accepted",LineOrder)
                        #time.sleep(5)
                        InsertTools.InsertDICTIONNARY(ListFunction,ID)
                        #time.sleep(5)
                        InsertTools.ChangeCOMMANDS("done",LineOrder)
                        #time.sleep(5)

                    if('TEMPERATURE' in Function):
                        print("TEMPERATURE")
                        InsertTools.ChangeCOMMANDS("accepted",LineOrder)
                        zone=str(int(Function[-2]))
                        #temperatureValue='tempOf'+zone
                        #For jetson
                        temperatureValue=0.001*int(subprocess.check_output("cat /sys/devices/virtual/thermal/thermal_zone"+zone+"/temp", shell=True))
                        temperatureValue=str(temperatureValue)
                        InsertTools.UpdateCom(temperatureValue,LineOrder)
                        InsertTools.ChangeCOMMANDS("done",LineOrder)

                    if('CIRCLE' in Function):
                        print("TEMPERATURE")
                        InsertTools.ChangeCOMMANDS("accepted",LineOrder)
                        PubForHeron.Circle()
                        InsertTools.ChangeCOMMANDS("done",LineOrder)
