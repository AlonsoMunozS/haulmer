#! /usr/bin/python
import mysql.connector
from mysql.connector import Error
import sys
import json

def get_status_db(data_connection):
    status=-1
    db=data_connection['DB']
    user=data_connection['USER']
    psw=data_connection['PASSWORD']
    host=data_connection['HOST']
    #print ("db: " + db +", user: "+ user +", password: " + psw + ", host: "+host)
    
                                 
    try:
        conn = mysql.connector.connect(host=host,
                                    database=db,
                                    user=user,
                                    password=psw,
                                    port=3306) 
        if conn.is_connected():
            conn.close()
            #print('Connected to MySQL database')
            status=1
    except Error as e:
        pass
    return status
def get_data_connection(id):
    with open('/tmp/json_mysql.json', 'r') as f:
        data = json.load(f)
        for app_id in data:
            if app_id==id:
                return data[id]


status=-1
if sys.argv[1] != "":
    data_connection=get_data_connection(sys.argv[1])
    status=get_status_db(data_connection)
print status

