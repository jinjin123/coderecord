#coding=utf-8
import pymysql
import pymysql.cursors

class MYSQL:
    """
    对pymysql的简单封装
    """
    def __init__(self,host,user,pwd,port,db):
        self.host = 'localhost'
	self.port = 3306
        self.user = 'root'
        self.pwd = ''
        self.db = 'Automating'

    def __GetConnect(self):
        """
        得到连接信息
        返回: conn.cursor()
        """
        if not self.db:
            raise(NameError,"没有设置数据库信息")
        self.conn = pymysql.connect(host=self.host,user=self.user,password=self.pwd,port=self.port,database=self.db,charset='utf8',cursorclass=pymysql.cursors.DictCursor)
        cur = self.conn.cursor()
        if not cur:
            raise(NameError,"连接数据库失败")
        else:
            return cur
	#插入语句是从缓存里面插的要commit()才能生效
    def ExecNonQuery(self,sql):
            cur = self.__GetConnect()
            cur.execute(sql)
            self.conn.commit()
            self.conn.close()
	#查询语句是直接可以查的无需commit 如果在缓存里面使用查询语句返回的是None
    def ExecQuery(self,sql):
		cur = self.__GetConnect()
		cur.execute(sql) 
		resList = cur.fetchall()
                self.conn.close()
                return resList
	
def main():
 	mysql = MYSQL(host="localhost",port=3306,user="root",pwd="",db="Automating")
	#mysql.ExecNonQuery("insert into user_a values(3,'a','b','c','d',NOW())")
    	mysql.ExecQuery("USE Automating")
   	mysql.ExecQuery("create table user_a(id int not null auto_increment PRIMARY KEY, name VARCHAR(18) not null,password VARCHAR(32) not null,class VARCHAR(18) not null,descript VARCHAR(30) null,time timestamp  not NULL  default CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP)")

	

if __name__ == "__main__":
	main()
