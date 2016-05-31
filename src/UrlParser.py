# -*- coding: utf-8 -*-
import re
from pymysql import Connection

HOST = 'localhost'
USER='root'
PASSWORD='admin'
DATABASE='policyDB'
PORT= 3306
CHARSET = 'utf8mb4'
connection = Connection(host=HOST,user=USER,password=PASSWORD,database=DATABASE,port=PORT,charset=CHARSET)
cursor = connection.cursor()

sql = "select url from url";
cursor.execute(sql)

rs = cursor.fetchall()
insertdate = ''
for rec in rs:
   reclist = rec[0].split("/")
   insertdate = reclist[-2][0:4]+'-'+reclist[-2][4:]
   sql1 = 'insert into recTime(pubTime) values(%s)'
   cursor.execute(sql1,(insertdate))
   connection.commit()

print "SUCCESS"  
connection.close()
   