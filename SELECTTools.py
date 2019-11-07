# -*- coding: utf-8 -*-

from InsertTools import CountID
import mysql.connector

def SELECT(table):

    connection = mysql.connector.connect(host='localhost',database='heronDatabase',user='robot',password='HeronLeR0B0T')
    sql_select_Query = "select * from "+table+" ;"
    print(sql_select_Query)
    cursor = connection.cursor()
    cursor.execute(sql_select_Query)
    records = cursor.fetchall()
    #{print("la longueur : ",len(records))
    if (connection.is_connected()):
            connection.close()
            cursor.close()
    return records

def CommandsFor(ID):#Return LineOrder-OrderID-Function-Target-Status-Source-Com
    L=[]
    for elt in SELECT("AVAILABLE"):
        if(elt[1]==ID):
            L.append(elt)
    return(L)

def FunctionOrdered(ID):
    return(SELECT("AVAILABLE","ID='"+ID+"''"))

for i in(CommandsFor("test-0-1")):
    print(i)
