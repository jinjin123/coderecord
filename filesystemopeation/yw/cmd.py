#-*- coding: utf-8 -*-  
#!/usr/bin/python   
import paramiko  
import threading  
import time
import sys
reload(sys) 
sys.setdefaultencoding('utf8')

class REMOTE:
	def __init__(self,ip,port,username,passwd,cmd,timeout=None):
		self.ip = ip
		self.port = port
		self.username = username
		self.passwd = passwd
		self.cmd = cmd
		self.timeout = None
		
		
        def ssh2(self,ip,port,username,passwd,cmd,timeout=5):  
               try:
                    global file
                    ssh = paramiko.SSHClient()
                    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                    ssh.connect(ip,port,username,passwd,timeout=5)
                    for m in cmd:
                                file = open('/root/yw/cmd_return.txt','a+')
                                stdin, stdout, stderr = ssh.exec_command(m)
                                out = stdout.readlines()
                                file.write('%s \n'%(ip))
                                #print ip
                                for o in out:
                                           try:
                                              # print o
                                               file.write('%s'%(o))
                                               ssh.close()

                                           except:
                                                  print "ERROR"
               except:
			print "ERROR"
                      #file.write('%s\tError\r'%(ip))
                      #time.sleep(15)
                      #file.close()


if __name__=='__main__':  
	pc = REMOTE(ip='',port=22,username='',passwd='',cmd='',timeout=5)
	username = 'root'
	passwd = 'jinjin123'
	cmd = ['df -h']
	threads = []
	print "begin.."
	for i in range(1,9):
		ip = '192.168.1.'+str(i)
		a=threading.Thread(target=pc.ssh2,args=(ip,22,username,passwd,cmd))
		a.start()

	print "ok"
	

"""
    cmd = ['df -h']#你要执行的命令列表  
    username = "root"  #用户名  
    port = 22
    passwd = "jinjin123"    #密码  
    threads = []   #多线程  
    print "Begin......" 
    for i in range(1,100):  
        ip = '192.168.1.'+str(i)  
        a=threading.Thread(target=ssh2,args=(ip,int(port),username,passwd,cmd))   
        a.start() 
"""
