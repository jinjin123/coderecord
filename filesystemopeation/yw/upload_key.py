#!/usr/bin/env python # -*- coding: utf-8 -*-  
import sys,os
import paramiko
import threading
reload(sys) 
sys.setdefaultencoding('utf8')

class UPLOAD:
	def __init__(self,host,port,user,passwd):
		self.host = host
		self.port = port
		self.user = user
		self.passwd = passwd

	#使用密码上传密钥
	def up_key(self,host,port,user,passwd):
			home_dir = '/root'
			id_rsa_pub = '%s/.ssh/id_rsa.pub' %home_dir

			if not  id_rsa_pub:
				print 'id_rsa.pub Does not exist!'
				sys.exit(0)
			file_object = open('%s/.ssh/config' %home_dir ,'a')
			file_object.write('StrictHostKeyChecking no\n')
			file_object.write('UserKnownHostsFile /dev/null')
			file_object.close()
			try:
                                s = paramiko.SSHClient()
	                        s.set_missing_host_key_policy(paramiko.AutoAddPolicy())
	                        s.connect(host,port,user, passwd)
                                t = paramiko.Transport((host,port))
                                t.connect(username=user, password=passwd)
                                sftp =paramiko.SFTPClient.from_transport(t)

				try:
					f = open('/root/yw/log.txt','a+')
					f.write('create Host:%s .ssh dir...\r' %host)
					print 'create Host:%s .ssh dir...\r' %host
                                        stdin,stdout,stderr=s.exec_command('mkdir ~/.ssh/')
					f.write('upload id_rsa.pub to Host:%s...\r' %host)
					print 'upload id_rsa.pub to Host:%s...\r' %host
                                        sftp.put(id_rsa_pub, "/tmp/temp_key")
                                        stdin,stdout,stderr=s.exec_command('cat /tmp/temp_key >> ~/.ssh/authorized_keys && rm -rf /tmp/temp_key')
					f.write('host:%s@%s auth success!\r' %(user,host))
					print 'host:%s@%s auth success!\r' %(user,host)
					f.close()
                                        s.close()
                                        t.close()
				except:
					pass
                        except Exception, e:
                                    import traceback
                                    traceback.print_exc()
                                    try:
                                       s.close()
                                       t.close()
                                    except:
                                        pass
	#使用密码上传文件
	def sftp_put(self,host,port,user,passwd,localpath=None,remotepath=None):
        	t = paramiko.Transport((host,port))
        	t.connect(username=user,password=passwd)
        	sftp = paramiko.SFTPClient.from_transport(t)
        	sftp.put(localpath=localpath,remotepath=remotepath)
        	print host,localpath,remotepath
		t.close()

	#使用密码下载文件
	def sftp_down(self,host,port,user,passwd,remotepath=None,localpath=None):
        	t = paramiko.Transport((host,port))
        	t.connect(username=user,password=passwd)
        	sftp = paramiko.SFTPClient.from_transport(t)
        	sftp.get(remotepath=remotepath,localpath=localpath)
		t.close()
        #	print host,remotepath,localpath
	#	t.close()
		

	#使用key密钥登录
	def ssh2_key(self,command=None):
        	paramiko.util.log_to_file('/tmp/paramiko.log') 
        	key = paramiko.RSAKey.from_private_key_file(self.key_file)    
        	ssh2 = paramiko.SSHClient()
        	ssh2.load_system_host_keys()
        	ssh2.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        	ssh2.connect(hostname=self.h,username=self.u,pkey=key,port=self.port,timeout=self.t)
        	stdin,stdout,stderr = ssh2.exec_command(command)
        	print '{0}\t{1}'.format(self.h,command)
        	print stdout.read()
        	ssh2.close()
	
	#使用key密钥上传文件
    	def sftp_key_put(self,localpath=None,remotepath=None):
        	key = paramiko.RSAKey.from_private_key_file(self.key_file)    
        	t = paramiko.Transport((self.h,self.port))
        	t.connect(username=self.u,pkey=key)
        	sftp = paramiko.SFTPClient.from_transport(t)
        	sftp.put(localpath=localpath,remotepath=remotepath)
        	print self.h,localpath
        	t.close()
"""
		try:
			f = open('/root/yw/fileup.txt','a+')
			f.write('%s,%s,%s upload succesfull\r' %(host,localpath,remotepath))
        		print host,localpath,remotepath
			f.close()
		except:
			print "error"
        	t.close()
"""

def run():
	upload = UPLOAD(host='',port='',user='',passwd='')
	remotepath = '/root/1'
	localpath = '/tmp/1'
	for line in open('/root/yw/host.list'):
		line = line.strip('\n')
		host,port,user,passwd = line.split(':')
		a=threading.Thread(target=upload.sftp_down,args=(host,int(port),user,passwd,remotepath,localpath))
		a.start()
"""
def run():
	upload = UPLOAD(host='',port='',user='',passwd='')
	for line in open('/root/yw/host.list'):
		line = line.strip('\n')
		host,port,user,passwd = line.split(':')
		a=threading.Thread(target=upload.up_key,args=(host,int(port),user,passwd))
		a.start()
"""
if __name__ == '__main__':
    run()
