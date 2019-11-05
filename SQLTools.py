# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""


import mysql.connector
import os
import time

def InsertID(askedname):
    askedname=FindID(askedname)
    try:
        connection = mysql.connector.connect(host='localhost',database='heronDatabase',
        user='root',password='HeronLeR0B0T')

        mySql_insert_query = """INSERT INTO AVAILABLE (Id, Status, ComAvailable)
                               VALUES
                               ('"""+askedname+"""', 'available', 'LastTest') """

        cursor = connection.cursor()
        result = cursor.execute(mySql_insert_query)
        connection.commit()
        cursor.close()

    except mysql.connector.Error as error:
        print("Failed to insert record into AVAILABLE {}".format(error))

    return askedname

def InsertCOMMANDS(destination,function,source,com=None):
    try:
        connection = mysql.connector.connect(host='localhost',database='heronDatabase',
        user='root',password='HeronLeR0B0T')
        if(com!=None):
            mySql_insert_query = "INSERT INTO COMMANDS (OrderId, Function,Target,Status,Source,ComOrder) VALUES ('ToDo','"+function+"','"+destination+"','waiting','"+source+"','"+com+"');"
        else:
            mySql_insert_query = "INSERT INTO COMMANDS (OrderId, Function,Target,Status,Source) VALUES ('ToDo','"+function+"','"+destination+"','waiting','"+source+"');"

        print("sql insert query")
        print(mySql_insert_query)
        cursor = connection.cursor()
        result = cursor.execute(mySql_insert_query)
        connection.commit()
        cursor.close()

    except mysql.connector.Error as error:
        print("Failed to insert record into AVAILABLE {}".format(error))

    return True

def CountID(condition):

    try:
        connection = mysql.connector.connect(host='localhost',database='heronDatabase',
        user='root',password='HeronLeR0B0T')

        sql_select_Query = "select * from AVAILABLE where "+condition+";"
        cursor = connection.cursor()
        cursor.execute(sql_select_Query)
        records = cursor.fetchall()
        #{print("la longueur : ",len(records))
        for row in records:
            #print(row)
            pass
    except :
        print("Error reading data from MySQL table")

    finally:
        if (connection.is_connected()):
            connection.close()
            cursor.close()
    return len(records)


def DisplayOneTime(table):
    try:
        connection = mysql.connector.connect(host='localhost',database='heronDatabase',user='root',password='HeronLeR0B0T')

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
