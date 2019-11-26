# -*- coding: utf-8 -*-
#!/usr/bin/env python
"""
@author: Quentin
"""

from InsertTools import CountID
from InsertTools import ChangeCOMMANDS
from InsertTools import InsertDICTIONNARY
import mysql.connector
import sys


Function=[['DICTIONNARY','DICTIONNARY',''],['PRINT','PRINT(str)','PRINT ON DEVICE'],['TEMPERATURE','TEMPERATURE','Return in Comm the TEMPERATURE']]

def SELECT(table,condition=""):#Retourne sous la forme d'une liste les résultat une requete sql SELECT * FROM table;

    if(condition!=''):
        condition="where "+condition

    try:
        connection = mysql.connector.connect(host='10.224.0.52',database='heronDatabase',user='robot',password='HeronLeR0B0T')
        sql_select_Query = "SELECT * FROM "+table+" "+condition+";"
        #print(sql_select_Query)
        #print(sql_select_Query)
        cursor = connection.cursor()
        cursor.execute(sql_select_Query)
        records = cursor.fetchall()
        #{print("la longueur : ",len(records))
        if (connection.is_connected()):
                connection.close()
                cursor.close()
        return records

    except:
        print("Erreure durant un SELECT ,",table)
        print(sys.exc_info())

def CommandsFor(ID):#Retourne LineOrder-OrderID-Function-Target-Status-Source-Com destiné à L'ID spécifié
    L=[]
    for elt in SELECT("COMMANDS"):
        if(elt[3]==ID):
            L.append(elt)
    return(L)

def FunctionOrdered(ID):
    return(SELECT("COMMANDS","TARGET='"+ID+"''"))

#InsertDICTIONNARY(FunctionList,ID)#Liste de function [Function,ShortDesc,LongDesc]

#for elt in CommandsFor('raspberryMegaTest-1'):
#    print(elt[0],elt[2].encode("ascii"))
#    if(('DICTIONNARY' in elt[2].encode('ascii') and (elt[4].encode('ascii')=='waiting'))):
#        InsertDICTIONNARY(Function,'raspberryMegaTest-1')
#        ChangeCOMMANDS('accepted',elt[0])
    #ChangeCOMMANDS('Done',elt[0])
