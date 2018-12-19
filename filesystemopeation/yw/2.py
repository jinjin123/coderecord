#coding=utf-8
import pymysql
import pymysql.cursors
try:

    conn=pymysql.connect(host='localhost',port=3306,user='root',passwd='',charset='UTF8',cursorclass=pymysql.cursors.DictCursor)
    #conn=pymysql.connect(host=‘localhost‘,user=‘root‘,passwd=‘‘,db=‘bookdb‘)
    cur=conn.cursor()                              #获取一个游标对象
    cur.execute("CREATE DATABASE test15")          #执行对应的SQL语句
    cur.execute("USE test15")   #创建数据库
    cur.execute("CREATE TABLE users1 (id INT, name VARCHAR(18))")#创建表
    cur.execute("INSERT INTO users1 VALUES(1,'blog'),(2,'csd'),(3,'aa')")

    cur.execute("SELECT * FROM users1")
    data=cur.fetchall()

    for row in data:
	print type(row)
	print('%s'%row)


    cur.close()                                    #关闭游标
    conn.commit()                                  #向数据库中提交任何未解决的事务，对不支持事务的数据库不进行任何操作
    conn.close()                                   #关闭到数据库的连接，释放数据库资源
except Exception :print("发生异常")
