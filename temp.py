# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""


import mysql.connector 


def InsertID(askedname):
    askedname=FindID(askedname)
    try:
        connection = mysql.connector.connect(host='localhost',database='heronDatabase',user='root',password='HeronLeR0B0T')
                                             
        mySql_insert_query = """INSERT INTO AVAILABLE (Id, Status, ComAvailable) 
                               VALUES 
                               ('"""+askedname+"""', 'available', 'LastTest') """
    
        cursor = connection.cursor()
        result = cursor.execute(mySql_insert_query)
        connection.commit()
        print("Record inserted successfully into Laptop table")
        cursor.close()
    
    except mysql.connector.Error as error:
        print("Failed to insert record into AVAILABLE {}".format(error))
        
    return True
    
    #if (connection.is_connected()):
    #    connection.close()
    #    print("MySQL connection is closed")
    
def CountID(condition):
    
    try:
        connection = mysql.connector.connect(host='localhost',database='heronDatabase',user='root',password='HeronLeR0B0T')
    
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
    
def FindID(name):
    i=1
    while(CountID("ID='"+name+"-"+str(i)+"'")):
        i+=1
    return name+"-"+str(i)
