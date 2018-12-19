#coding=utf-8
from mysql import *

#try:
#       MYSQL.ExecNonQuery("show * FROM user_a;")
#except Exception:
#       print("建表失败")

def Getdata():
        mysql = MYSQL(host="localhost",port=3306,user="root",pwd="",db="Automating")
        userdata = mysql.ExecQuery("SELECT ID,HOST from  myhost")
	for i in userdata:
		print i[u'HOST']
		print i.keys()
		print type(i)

if __name__ == "__main__":
	Getdata()
