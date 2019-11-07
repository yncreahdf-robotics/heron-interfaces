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
        user='robot',password='HeronLeR0B0T')
        if(com!=None):
            mySql_insert_query = "INSERT INTO COMMANDS (OrderId, Function,Target,Status,Source,ComOrder) VALUES ('ToDo','"+function+"','"+destination+"','waiting','"+source+"','"+com+"');"
        else:
            mySql_insert_query = "INSERT INTO COMMANDS (OrderId, Function,Target,Status,Source) VALUES ('ToDo','"+function+"','"+destination+"','waiting','"+source+"');"

        #print("sql insert query")
        #print(mySql_insert_query)
        cursor = connection.cursor()
        result = cursor.execute(mySql_insert_query)
        connection.commit()
        cursor.close()

    except mysql.connector.Error as error:
        print("Failed to insert record into AVAILABLE {}".format(error))

    return True

def InsertDICTIONNARY(FunctionList,ID):
    for elt in FunctionList:
            function,shortDescription,longDescription=elt[0],elt[1],elt[2]
            connection = mysql.connector.connect(host='localhost',database='heronDatabase',
            user='robot',password='HeronLeR0B0T')
            mySql_insert_query = "INSERT INTO DICTIONNARY (ID,Function, ShortDescription,LongDescription) VALUES ('"+ID+"','"+function+"','"+shortDescription+"','"+longDescription+"');"
            cursor = connection.cursor()
            result = cursor.execute(mySql_insert_query)
            connection.commit()
            cursor.close()

listFunction=[["function 1","shortDescription1","longDesciption1"],["function 2","shortDescription2","longDesciption2"]]
ID="centraltest-01"

InsertDICTIONNARY(listFunction,ID)
