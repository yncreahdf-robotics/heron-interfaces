# -*- coding: utf-8 -*-
#!/usr/bin/env python
"""
@author: Quentin
"""

import mysql.connector
import os
import time


def FindID(name):
    print(CountID(name))
    return (name+"-"+str(CountID(name)))

def CountID(name):#retourne le premier indice libre d'un nom. i.e. si heron-1 et heron-2 sont déjà utilisé CountID("heron") retourne 3

    connection = mysql.connector.connect(host='10.224.0.52',database='heronDatabase',
    user='robot',password='HeronLeR0B0T')
    sql_select_Query = "select * from AVAILABLE;"
    cursor = connection.cursor()
    cursor.execute(sql_select_Query)
    records = cursor.fetchall()

    #On recherche le premier index libre pour cet ID
    Test=True
    it=1 #Il est au minimum 1
    while(Test):#Tant qu'il est nescessaire de continuer
        Test=False #On suppose avoir trouvé le premier index libre
        for elt in records:
            if(elt[1]==name+"-"+str(it)): #Si l'index est utilisé
                Test=True #Alors on doit parcourir une nouvelle fois la boucle
                it+=1 #Et on incrémente donc l'indice
    return(it)


def InsertID(askedname):#Utilise CountID pour trouver l'indice à utiliser. Insert dans AVAILABLE le nom demandé + indice et retourne nom+"-"+ID à utiliser

    askedname=FindID(askedname)
    try:
        connection = mysql.connector.connect(host='10.224.0.52',database='heronDatabase',
        user='robot',password='HeronLeR0B0T')

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

def InsertCOMMANDS(ref,destination,function,source,com=None):#Insert dans COMMANDS (OrderID,Target,Function,Source,ComOrder). ComOrder est facultatif, la commands serat automatiquement en wainting
    try:
        connection = mysql.connector.connect(host='10.224.0.52',database='heronDatabase',
        user='robot',password='HeronLeR0B0T')
        if(com!=None):
            mySql_insert_query = "INSERT INTO COMMANDS (OrderId, Function,Target,Status,Source,ComOrder) VALUES ('"+ref+"','"+function+"','"+destination+"','waiting','"+source+"','"+com+"');"
        else:
            mySql_insert_query = "INSERT INTO COMMANDS (OrderId, Function,Target,Status,Source) VALUES ('"+ref+"','"+function+"','"+destination+"','waiting','"+source+"');"

        cursor = connection.cursor()
        result = cursor.execute(mySql_insert_query)
        connection.commit()
        cursor.close()

    except mysql.connector.Error as error:
        print("Failed to insert record into AVAILABLE {}".format(error))

    return True

def InsertDICTIONNARY(FunctionList,ID):#Liste de function [Function,ShortDesc,LongDesc]

    connection = mysql.connector.connect(host='10.224.0.52',database='heronDatabase',
    user='robot',password='HeronLeR0B0T')
    mySql_insert_query = "DELETE FROM DICTIONNARY where ID='"+ID+"';"
    cursor = connection.cursor()
    result = cursor.execute(mySql_insert_query)
    connection.commit()
    cursor.close()

    for elt in FunctionList:
            function,shortDescription,longDescription=elt[0],elt[1],elt[2]
            connection = mysql.connector.connect(host='10.224.0.52',database='heronDatabase',
            user='robot',password='HeronLeR0B0T')
            mySql_insert_query = "INSERT INTO DICTIONNARY (ID,Function, ShortDescription,LongDescription) VALUES ('"+ID+"','"+function+"','"+shortDescription+"','"+longDescription+"');"
            cursor = connection.cursor()
            result = cursor.execute(mySql_insert_query)
            connection.commit()
            cursor.close()

def ChangeCOMMANDS(status,line):#Change le status de la ligne de clé primaire line

    #Pour des raisons encore obscures, si les INSERT fonctionnent, les UPDATE eux nescessitent de passer par la console
    line=str(line)
    connection = mysql.connector.connect(host='10.224.0.52',database='heronDatabase',user='robot',password='HeronLeR0B0T')
    sql_select_Query = 'UPDATE heronDatabase.COMMANDS SET STATUS="'
    sql_select_Query +=status
    sql_select_Query += '" where LineOrder="'
    sql_select_Query += line
    sql_select_Query +='"'

    cmd="""mysql -u 'robot' -h '10.224.0.52' --password='HeronLeR0B0T' -e '"""#Execute the UPDATE with a command line in a terminale
    cmd+=sql_select_Query
    cmd+="'"

    os.system(cmd)#On execute la commande dans la console

    cursor = connection.cursor()
    cursor.execute(sql_select_Query)
    if (connection.is_connected()):
            connection.close()
            cursor.close()

def UpdateCom(com,line):#Change le status de la ligne de clé primaire line

    #Pour des raisons encore obscures, si les INSERT fonctionnent, les UPDATE eux nescessitent de passer par la console
    line=str(line)
    connection = mysql.connector.connect(host='10.224.0.52',database='heronDatabase',user='robot',password='HeronLeR0B0T')
    sql_select_Query = 'UPDATE heronDatabase.COMMANDS SET ComOrder="'
    sql_select_Query +=com
    sql_select_Query += '" where LineOrder="'
    sql_select_Query += line
    sql_select_Query +='"'

    cmd="""mysql -u 'robot' -h '10.224.0.52' --password='HeronLeR0B0T' -e '"""#Execute the UPDATE with a command line in a terminale
    cmd+=sql_select_Query
    cmd+="'"

    os.system(cmd)#On execute la commande dans la console

    cursor = connection.cursor()
    cursor.execute(sql_select_Query)
    if (connection.is_connected()):
            connection.close()
            cursor.close()
