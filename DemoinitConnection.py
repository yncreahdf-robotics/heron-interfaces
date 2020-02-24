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
    
def openFile(mode):
    return open("/home/centralheron/MapKeyPos.txt", mode)
    
def load():
    file = openFile("r")
    content = file.readlines()
    file.close()
    if(len(content) == 0):
        sys.exit()

    lines = content[1::]
    
    Ret=[]

    for line in lines:
        name = line.split(":")[0]
        x = float(line.split(":")[1].split(";")[0])
        y = float(line.split(":")[1].split(";")[1])
        z = float(line.split(":")[1].split(";")[2])
        w = float(line.split(":")[1].split(";")[3])
        h = float(line.split(":")[1].split(";")[4].split("\n")[0])
        Ret.append([name,x,y,z,w,h])
        
    return Ret
        
    

def InitConnection(name):

    Server = '192.168.0.105' #IP du Server
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

#ID=InitConnection("heron")



print("----------------------")


now=time.time()
while(time.time()-now<600):
    InsertTools.InsertCOMMANDS(HERON_ID,HERON_ID,"DEMOSPRINT","Central",com=None)
    itDemo=0
    commands=SELECTTools.CommandsFor(HERON_ID)
    
    for elt in commands:
        LineOrder,OrderID,Function,Target,Status,Source,ComOrder=elt[0],elt[1],elt[2],elt[3],elt[4],elt[5],elt[6]
        if(Status=='waiting'):
                if(Status=='waiting'):

                    if(Function=='DEMOSPRINT'):
                        InsertTools.ChangeCOMMANDS("accepted",LineOrder)
                        itDemo+=1
                        print("---------PHASE 1-----------")

                        ref1,ref2="DemoPhase1-"+str(itDemo)+"-Heron","DemoPhase1-"+str(itDemo)+"-Niryo"

                        #A décom
                        InsertTools.InsertCOMMANDS(ref2,"niryo-1","TAKE(STOCK,0)","Central",com=None)


                        
                        #status1=SELECTTools.SELECT("COMMANDS","OrderID='"+ref1+"'")[0][4]
                        
                        #A décom
                        status2=SELECTTools.SELECT("COMMANDS","OrderID='"+ref2+"'")[0][4]
                        
                        for pos in load():
                            if ('niryo-1' in pos[0]):
                                x,y,z,w,h=pos[1],pos[2],pos[3],pos[4],pos[5]
                                
                        PubForHeron.Zone(x,y,z,w,h,zone_publisher)
                        

                        #A décom
                        while(status2!='done'):


                            #status1=SELECTTools.SELECT("COMMANDS","OrderID='"+ref1+"'")[0][4]
                            #A décom
                            status2=SELECTTools.SELECT("COMMANDS","OrderID='"+ref2+"'")[0][4]

                            #print("status1 : ",status1)
                            #A décom
                            print("status2 : ",status2)
                            
                        ref2=ref2+"bis"
                        InsertTools.InsertCOMMANDS(ref2,"niryo-1","RELEASE()","Central",com=None)
                        
                        status2=SELECTTools.SELECT("COMMANDS","OrderID='"+ref2+"'")[0][4]
                        
                        while(status2!='done'):


                            #status1=SELECTTools.SELECT("COMMANDS","OrderID='"+ref1+"'")[0][4]
                            #A décom
                            status2=SELECTTools.SELECT("COMMANDS","OrderID='"+ref2+"'")[0][4]

                            #print("status1 : ",status1)
                            #A décom
                            print("status2 : ",status2)



                        print("---------PHASE 2-----------")

                        ref1="DemoPhase1b-"+str(itDemo)+"-Niryo"
                        #A décom
                        InsertTools.InsertCOMMANDS(ref1,"niryo-2","PREPARE(ROBOT)","Central",com=None)

                        #A décom
                        status1=SELECTTools.SELECT("COMMANDS","OrderID='"+ref1+"'")[0][4]

                        #A décom
                        while(status1!='done'):
                            #A décom
                            status1=SELECTTools.SELECT("COMMANDS","OrderID='"+ref1+"'")[0][4]

                        print("---------PHASE 3-----------")

                        #ref1="DemoPhase3-"+str(itDemo)+"-Heron"
                        #InsertTools.InsertCOMMANDS(ref1,"heron-1","ZONE(BANC)","Central",com=None)

                        #status1=SELECTTools.SELECT("COMMANDS","OrderID='"+ref1+"'")[0][4]

                        #while(status1!='done'):
                        #    status1=SELECTTools.SELECT("COMMANDS","OrderID='"+ref1+"'")[0][4]

                        for pos in load():
                            if ('niryo-2' in pos[0]):
                                x,y,z,w,h=pos[1],pos[2],pos[3],pos[4],pos[5]
                                
                        PubForHeron.Zone(x,y,z,w,h,zone_publisher)
                        

                        print("---------PHASE 4-----------")


                        #A décom
                        ref1="DemoPhase1b-"+str(itDemo)+"-Niryo"
                        #A décom
                        InsertTools.InsertCOMMANDS(ref1,"niryo-2","TAKE(ROBOT)","Central",com=None)

                        #A décom
                        status1=SELECTTools.SELECT("COMMANDS","OrderID='"+ref1+"'")[0][4]

                        #A décom
                        while(status1!='done'):
                            #A décom
                            status1=SELECTTools.SELECT("COMMANDS","OrderID='"+ref1+"'")[0][4]


                        print("---------PHASE 5-----------")

                        #ref1="DemoPhase5-"+str(itDemo)+"-Heron"
                        #InsertTools.InsertCOMMANDS(ref1,"heron-1","ZONE(BASE)","Central",com=None)

                        #status1=SELECTTools.SELECT("COMMANDS","OrderID='"+ref1+"'")[0][4]

                        #while(status1!='done'):
                        #    status1=SELECTTools.SELECT("COMMANDS","OrderID='"+ref1+"'")[0][4]

                        for pos in load():
                            if ('Base' in pos[0]):
                                x,y,z,w,h=pos[1],pos[2],pos[3],pos[4],pos[5]
                                
                        PubForHeron.Zone(x,y,z,w,h,zone_publisher)

                        InsertTools.ChangeCOMMANDS("done",LineOrder)




"""
now=time.time()
while(time.time()-now<600):
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
"""
print("end")