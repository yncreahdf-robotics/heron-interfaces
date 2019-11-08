# -*- coding: utf-8 -*-

from InsertTools import CountID
import mysql.connector
import sys

def SELECT(table,condition=""):#Retourne sous la forme d'une liste les résultat une requete sql SELECT * FROM table;

    if(condition!=''):
        condition="where "+condition

    try:
        connection = mysql.connector.connect(host='localhost',database='heronDatabase',user='robot',password='HeronLeR0B0T')
        sql_select_Query = "SELECT * FROM "+table+" "+condition+";"
        print(sql_select_Query)
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
