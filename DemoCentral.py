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


#from geometry_msgs.msg import Twist
#from std_msgs.msg import Bool
#from heron.msg import Motion


HERON_ID='Heron01'

#rospy.init_node('centralheron', anonymous=True)
#velocity_publisher = rospy.Publisher('/'+HERON_ID+'/cmd_vel', Twist, queue_size=10)
#zone_publisher = rospy.Publisher('/'+HERON_ID+'/move_to', Motion, queue_size=10)
#rospy.sleep(1)

#import PubForHeron

#import rospy
#from std_msgs.msg import String

HERON_ID='Heron01'


#ListFunction=[['DICTIONNARY','DICTIONNARY',''],
#['TEMPERATURE','TEMPERATURE(nZone)','Return in Comm the TEMPERATURE of the zone : BCPU-therm / MCPU-therm / GPU-therm / PLL-therm / Tboard_tegra / Tdiode_tegra / PMIC-Die / thermal-fan-est'],
#['CIRCLE','CIRCLE',''],['ZONE','ZONE(ZoneName)','Send Robot to the zone named "BANC", "BASE", "STOCK"']]




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

ID=InitConnection("central")

print("----------------------")

#InsertTools.InsertCOMMANDS('fortheTest',ID,'TEMPERATURE(4)','fortheTest',com=None)

now=time.time()
itDemo=0
while(time.time()-now<300):
    commands=SELECTTools.CommandsFor(ID)
    for elt in commands:
        LineOrder,OrderID,Function,Target,Status,Source,ComOrder=elt[0],elt[1],elt[2],elt[3],elt[4],elt[5],elt[6]
        if(Status=='waiting'):
                if(Status=='waiting'):

                    if(Function=='DEMOSPRINT'):
                        InsertTools.ChangeCOMMANDS("accepted",LineOrder)
                        itDemo+=1
                        print("---------PHASE 1-----------")

                        ref1,ref2="DemoPhase1-"+str(itDemo)+"-Heron","DemoPhase1-"+str(itDemo)+"-Niryo"


                        InsertTools.InsertCOMMANDS(ref1,"heron-1","ZONE(STOCK)","Central",com=None)
                        InsertTools.InsertCOMMANDS(ref2,"niryo-1","TAKE(0,0)","Central",com=None)


                        print("avant")
                        status1=SELECTTools.SELECT("COMMANDS","OrderID='"+ref1+"'")[0][4]
                        status2=SELECTTools.SELECT("COMMANDS","OrderID='"+ref2+"'")[0][4]
                        print("after")

                        while(status1!='done' or status2!='done'):


                            status1=SELECTTools.SELECT("COMMANDS","OrderID='"+ref1+"'")[0][4]
                            status2=SELECTTools.SELECT("COMMANDS","OrderID='"+ref2+"'")[0][4]

                            print("status1 : ",status1)
                            print("status2 : ",status2)



                        print("---------PHASE 2-----------")

                        ref1="DemoPhase1b-"+str(itDemo)+"-Niryo"
                        InsertTools.InsertCOMMANDS(ref1,"niryo-1","PREPARE(1)","Central",com=None)

                        status1=SELECTTools.SELECT("COMMANDS","OrderID='"+ref1+"'")[0][4]

                        while(status1!='done'):
                            status1=SELECTTools.SELECT("COMMANDS","OrderID='"+ref1+"'")[0][4]

                        print("---------PHASE 3-----------")

                        ref1="DemoPhase3-"+str(itDemo)+"-Heron"
                        InsertTools.InsertCOMMANDS(ref1,"heron-1","ZONE(BANC)","Central",com=None)

                        status1=SELECTTools.SELECT("COMMANDS","OrderID='"+ref1+"'")[0][4]

                        while(status1!='done'):
                            status1=SELECTTools.SELECT("COMMANDS","OrderID='"+ref1+"'")[0][4]


                        print("---------PHASE 4-----------")

                        ref1="DemoPhase1b-"+str(itDemo)+"-Niryo"
                        InsertTools.InsertCOMMANDS(ref1,"niryo-2","PREPARE(1)","Central",com=None)

                        status1=SELECTTools.SELECT("COMMANDS","OrderID='"+ref1+"'")[0][4]

                        while(status1!='done'):
                            status1=SELECTTools.SELECT("COMMANDS","OrderID='"+ref1+"'")[0][4]


                        print("---------PHASE 5-----------")

                        ref1="DemoPhase5-"+str(itDemo)+"-Heron"
                        InsertTools.InsertCOMMANDS(ref1,"heron-1","ZONE(BASE)","Central",com=None)

                        status1=SELECTTools.SELECT("COMMANDS","OrderID='"+ref1+"'")[0][4]

                        while(status1!='done'):
                            status1=SELECTTools.SELECT("COMMANDS","OrderID='"+ref1+"'")[0][4]

                        InsertTools.ChangeCOMMANDS("done",LineOrder)
