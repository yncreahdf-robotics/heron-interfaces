import mysql.connector
import os
import time


def DisplayOneTime(table):
    try:
        connection = mysql.connector.connect(host='localhost',database='heronDatabase',user='robot',password='HeronLeR0B0T')

        sql_select_Query = "select * from "+table+";"
        cursor = connection.cursor()
        cursor.execute(sql_select_Query)
        records = cursor.fetchall()
        #{print("la longueur : ",len(records))
        phr=""
        for row in records:
            for elt in row:
                phr=phr+str(elt)+"|"
            print(phr)
            phr=""
    except AssertionError as error:
        print(error)
        print("Error reading data from MySQL table")

    finally:
        if (connection.is_connected()):
            connection.close()
            cursor.close()


def Display(table,temp):#temp en second

    while(True):
        os.system("clear")
        DisplayOneTime(table)
        time.sleep(temp)

def DisplayAVAILABLE():
    Display("AVAILABLE",0.5)

def DisplayCOMMANDS():
    Display("COMMANDS",0.5)

def DisplayDICTIONNARY():
    Display("DICTIONNARY",0.5)

def FindID(name):
    i=1
    while(CountID("ID='"+name+"-"+str(i)+"'")):
        i+=1
    return name+"-"+str(i)

def main(a,b,c=None):
    print(a,b,c)
