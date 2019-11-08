import mysql.connector
import os
import time


def FindID(name):
    print(CountID(name))
    return (name+"-"+str(CountID(name)))

def CountID(name):#retourne le premier indice libre d'un nom. i.e. si heron-1 et heron-2 sont déjà utilisé CountID("heron") retourne 3

    connection = mysql.connector.connect(host='localhost',database='heronDatabase',
    user='robot',password='HeronLeR0B0T')
    sql_select_Query = "select * from AVAILABLE;"
    cursor = connection.cursor()
    cursor.execute(sql_select_Query)
    records = cursor.fetchall()
    Test=True
    it=0
    while(Test):
        Test=False
        for elt in records:
            if(elt[1]==name+"-"+str(it)):
                Test=True
                it+=1

    return(it)

def InsertID(askedname):#Utilise CountID pour trouver l'indice à utiliser. Insert dans AVAILABLE le nom demandé + indice et retourne nom+"-"+ID à utiliser
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

def InsertCOMMANDS(ref,destination,function,source,com=None):#Insert dans COMMANDS (OrderID,Target,Function,Source,ComOrder). ComOrder est facultatif, la commands serat automatiquement en wainting
    try:
        connection = mysql.connector.connect(host='localhost',database='heronDatabase',
        user='robot',password='HeronLeR0B0T')
        if(com!=None):
            mySql_insert_query = "INSERT INTO COMMANDS (OrderId, Function,Target,Status,Source,ComOrder) VALUES ('"+ref+"','"+function+"','"+destination+"','waiting','"+source+"','"+com+"');"
        else:
            mySql_insert_query = "INSERT INTO COMMANDS (OrderId, Function,Target,Status,Source) VALUES ('"+ref+"','"+function+"','"+destination+"','waiting','"+source+"');"

        #print("sql insert query")
        #print(mySql_insert_query)
        cursor = connection.cursor()
        result = cursor.execute(mySql_insert_query)
        connection.commit()
        cursor.close()

    except mysql.connector.Error as error:
        print("Failed to insert record into AVAILABLE {}".format(error))

    return True

def InsertDICTIONNARY(FunctionList,ID):#Liste de function [Function,ShortDesc,LongDesc]
    for elt in FunctionList:
            function,shortDescription,longDescription=elt[0],elt[1],elt[2]
            connection = mysql.connector.connect(host='localhost',database='heronDatabase',
            user='robot',password='HeronLeR0B0T')
            mySql_insert_query = "INSERT INTO DICTIONNARY (ID,Function, ShortDescription,LongDescription) VALUES ('"+ID+"','"+function+"','"+shortDescription+"','"+longDescription+"');"
            cursor = connection.cursor()
            result = cursor.execute(mySql_insert_query)
            connection.commit()
            cursor.close()

def ChangeCOMMANDS(status,line):#Change le status de la ligne de clé primaire line

    line=str(line)
    connection = mysql.connector.connect(host='localhost',database='heronDatabase',user='root',password='HeronLeR0B0T')
    sql_select_Query = 'UPDATE heronDatabase.COMMANDS SET STATUS="'
    sql_select_Query +=status
    sql_select_Query += '" where LineOrder="'
    sql_select_Query += line
    sql_select_Query +='"'

    #print(sql_select_Query)
    cmd="""mysql -u 'robot' --password='HeronLeR0B0T' -e '"""
    cmd+=sql_select_Query
    cmd+="'"
    #print("cmd:",cmd)
    os.system(cmd)
    #print(sql_select_Query)
    cursor = connection.cursor()
    #connection.commit()
    cursor.execute(sql_select_Query)
    #records = cursor.fetchall()
    #{print("la longueur : ",len(records))
    if (connection.is_connected()):
            connection.close()
            cursor.close()
