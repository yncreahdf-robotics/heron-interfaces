# -*- coding: utf-8 -*-

import mysql.connector
import os
import time

from DisplayTools import *
from InsertTools import *

def Clean(table):

    try:
        connection = mysql.connector.connect(host='localhost',database='heronDatabase',
        user='robot',password='HeronLeR0B0T')

        mySql_insert_query = "TRUNCATE TABLE "+table+";"

        cursor = connection.cursor()
        result = cursor.execute(mySql_insert_query)
        connection.commit()
        cursor.close()

    except mysql.connector.Error as error:
        print("Delet Fail")



    finally:
        if (connection.is_connected()):
            connection.close()
            cursor.close()
    return len(records)
