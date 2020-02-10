# -*- coding: utf-8 -*-
#!/usr/bin/env python
"""
@author: Quentin
"""

import mysql.connector
import os
import time


def DisplayOneTime(table):#Affiche une fois la table
    try:
        connection = mysql.connector.connect(host='10.224.0.52',database='heronDatabase',user='robot',password='HeronLeR0B0T')

        sql_select_Query = "select * from "+table+";"
        cursor = connection.cursor()
        cursor.execute(sql_select_Query)
        records = cursor.fetchall()
        #{print("la longueur : ",len(records))
    except AssertionError as error:
        print(error)
        print("Error reading data from MySQL table")

    finally:
        if (connection.is_connected()):
            connection.close()
            cursor.close()
    try:
        print("------",table,"-------")
        phr=""
        for row in records:
            for elt in row:
                phr=phr+str(elt)+"|"
            print(phr)
            phr=""
    except:
        print("Error during printing")

def Display(table,temp):#Affiche la table en boucle et actualise par défault toutes les 0.5 secondes (la période de rafraîchissement peut-être spécifiée en paramètre)
    while(True):
        os.system("clear")#On clear la console
        DisplayOneTime(table)#Affichage console
        time.sleep(temp)

def DisplayAVAILABLE(temps=0.5):
    Display("AVAILABLE",temps)

def DisplayCOMMANDS(temps=0.5):
    Display("COMMANDS",temps)

def DisplayDICTIONNARY(temps=0.5):
    Display("DICTIONNARY",temps)
