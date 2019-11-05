# -*- coding: utf-8 -*-

import mysql.connector
import os
import time

from DisplayTools import *
from InsertTools import *

def Clean(table):

    try:
        connection = mysql.connector.connect(host='localhost',database='heronDatabase',
        user='root',password='HeronLeR0B0T')

        mySql_insert_query = "TRUNCATE TABLE "+table+";"

        cursor = connection.cursor()
        result = cursor.execute(mySql_insert_query)
        connection.commit()
        cursor.close()

    except mysql.connector.Error as error:
        print("Delet Fail")

    return askedname

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
