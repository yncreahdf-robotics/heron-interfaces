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
import rospy

import PubForHeron

from geometry_msgs.msg import Twist
from std_msgs.msg import Bool
from heron.msg import Motion


HERON_ID='Heron01'

rospy.init_node('centralheron', anonymous=True)
velocity_publisher = rospy.Publisher('/'+HERON_ID+'/cmd_vel', Twist, queue_size=10)
zone_publisher = rospy.Publisher('/'+HERON_ID+'/move_to', Motion, queue_size=10)
rospy.sleep(1)



import PubForHeron

import rospy
from std_msgs.msg import String

HERON_ID='Heron01'


ListFunction=[['DICTIONNARY','DICTIONNARY',''],
['TEMPERATURE','TEMPERATURE(nZone)','Return in Comm the TEMPERATURE of the zone : BCPU-therm / MCPU-therm / GPU-therm / PLL-therm / Tboard_tegra / Tdiode_tegra / PMIC-Die / thermal-fan-est'],
['CIRCLE','CIRCLE',''],['ZONE','ZONE(ZoneName)','Send Robot to the zone named "BANC", "BASE", "STOCK"']]




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
while(time.time()-now<300):
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
                        PubForHeron.Circle(velocity_publisher)
                        InsertTools.ChangeCOMMANDS("done",LineOrder)

                    if('ZONE' in Function):

                        print("Zone")

                        if('BANC' in Function):
                            print("Banc")
                            position_x,position_y,orientation_z,orientation_w,plate_height=5.6612,3.9858,-0.9996,0.02776,0.79
                        if('BASE' in Function):
                            position_x,position_y,orientation_z,orientation_w,plate_height=4.55638,5.115,0.0839,0.0839,0.01
                            print("Base")
                        if('STOCK' in Function):
                            position_x,position_y,orientation_z,orientation_w,plate_height=5.8376,5.50369,0.73822,0.674549,0.787
                            print("Stock")

                        InsertTools.ChangeCOMMANDS("accepted",LineOrder)
                        PubForHeron.Zone(position_x,position_y,orientation_z,orientation_w,plate_height,zone_publisher)

                        InsertTools.ChangeCOMMANDS("done",LineOrder)
