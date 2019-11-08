import mysql.connector
import os
import time


def DisplayOneTime(table):#Affiche une fois la table
    try:
        connection = mysql.connector.connect(host='localhost',database='heronDatabase',user='robot',password='HeronLeR0B0T')

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
        phr=""
        for row in records:
            for elt in row:
                phr=phr+str(elt)+"|"
            print(phr)
            phr=""
    except:
        print("Error during printing")

def Display(table,temp):#temps en second, utilise DisplayOneTime en boucle et clean la console en
    while(True):
        os.system("clear")
        DisplayOneTime(table)
        time.sleep(temp)

def DisplayAVAILABLE(temps=0.5):
    Display("AVAILABLE",temps)

def DisplayCOMMANDS():
    Display("COMMANDS",temps)

def DisplayDICTIONNARY():
    Display("DICTIONNARY",temps)
