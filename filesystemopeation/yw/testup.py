# -*- coding=utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import tornado.web
import tornado.httpserver
import tornado.ioloop
import tornado.httpclient
import os.path,os,datetime
import threading
import paramiko
import urllib
from mysql import *
HTML = u""
	

	
class ssh():
    def __init__(self,host,user,pwd,remotepath=None,localpath=None,cmd=None,TYPE=None,port=22):
        self.host = host                #Hostname
        self.user = user                #用户名
        self.pwd = pwd                  #密码
        self.remotepath = remotepath    #远程路径，上传&下载文件时需要提供此参数
        self.localpath =  localpath     #本地路径，上传&下载文件时需要提供此参数
        self.port = port                #ssh端口
        self.cmd = cmd                  #需要在远程主机执行的命令，执行命令时需要提供此参数
        self.type = TYPE                #sftp操作类型，允许的值有两个：upload和download

    def ssh(self):      #命令执行
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(self.host,self.port,self.user,self.pwd,timeout=5)
        stdin, stdout, stderr = ssh.exec_command(self.cmd)
        return stdout.read()
        ssh.close()


    def sftp(self):     #文件上传下载
        t = paramiko.Transport((self.host,self.port))
        t.connect(username = self.user, password = self.pwd)
        sftp = paramiko.SFTPClient.from_transport(t)

        if self.type=='upload':
            sftp.put(self.localpath,self.remotepath)
        elif self.type=='download':
            sftp.get(self.remotepath, self.localpath)
        else:
            raise NameError('TYPE object is invalid!')
        t.close()
settings = {
    "static_path" : os.path.join(os.path.dirname(__file__), "static"),
    "template_path" : os.path.join(os.path.dirname(__file__), "templates"),
    "login_url": "/login",
    }

class main(tornado.web.RequestHandler):
    def get(self):
	mysql = MYSQL(host="localhost",port=3306,user="root",pwd="",db="Automating")
        SerList = mysql.ExecQuery("select ID,HOST from myhost")
	for i in SerList:
		print i
        if SerList:
            SerList = [(i[u'ID'],i[u'HOST']) for i in SerList]
        else:
            SerList = []
        self.render("test.html",**{"SerList":SerList})

    def post(self):
        global HTML
	cmd = self.get_argument('cmd',)
	argv = self.get_argument('argv',)
        TYPE = self.get_argument('TYPE',)
        filename = self.get_argument('localpath',)
        localpath = os.path.join(os.path.join(os.path.dirname(__file__),'files'),filename)
        remotepath = '%s/%s' % (self.get_argument('url',),filename)
        print remotepath,localpath
	mysql = MYSQL(host="localhost",port=3306,user="root",pwd="",db="Automating")
        HOST_LIST = mysql.ExecQuery("select HOST,USER,PWD from myhost WHERE ID in (%s)" % argv[0:-1])
        for i in HOST_LIST:
            t = execute(host = i[0],user = i[1],pwd = i[2],cmd = cmd,TYPE = TYPE,remotepath=remotepath,localpath=localpath)
            t.start()
            t.join()
        result = HTML
        HTML = u
        self.write(result)
class upload(tornado.web.RequestHandler):
    def post(self):
        upload_path=os.path.join(os.path.dirname(__file__),'files')
        file_metas=self.request.files['Filedata']
        filename=file_metas[0]['filename']
        filepath=os.path.join(upload_path,filename)
        with open(filepath,'wb') as up:
            up.write(file_metas[0]['body'])
        self.write('finished!')
class execute(threading.Thread):    #命令执行、文件上传下载任务并发执行。
    def __init__(self,host,user,pwd,cmd=None,TYPE='CMD',remotepath=None,localpath=None):
        threading.Thread.__init__(self)
        self.host = host
        self.user = user
        self.pwd = pwd
        self.cmd = cmd
        self.TYPE = TYPE
        self.remotepath = remotepath
        self.localpath = localpath
    def run(self):
        global HTML
        try:
            if self.TYPE=='CMD':
                result = ssh(host=self.host,user=self.user,pwd=self.pwd,cmd=self.cmd).ssh()
                if not result:result=u
                HTML = HTML + self.host + u':<br />' + result.strip() + u"<br />"
            elif self.TYPE=='UP':
                result = ssh(host=self.host,user=self.user,pwd=self.pwd,TYPE='upload',remotepath=self.remotepath,localpath=self.localpath).sftp()
                HTML = HTML + self.host + u'  :Upload successfull!<br />'
            else:
                raise NameError('TYPE object is invalid!')
        except Exception as e:
            pass

App = tornado.web.Application([
    (r'/',main),
    (r'/upload',upload),
    ],**settings)
if __name__ == "__main__":
    http_server=tornado.httpserver.HTTPServer(App)
    http_server.listen(80)
    tornado.ioloop.IOLoop.instance().start()
