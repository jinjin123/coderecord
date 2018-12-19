#!/usr/bin/env python
#coding:utf-8
 
import paramiko,sys,os,json
from multiprocessing import Pool
from mysql import *
 
def sftp_put(IP,Port,User,Locdir,Rmtdir):
    pravie_key_path = '/root/.ssh/id_rsa'
    key = paramiko.RSAKey.from_private_key_file(pravie_key_path)
    t = paramiko.Transport((IP,Port))
    t.connect(username=User,pkey=key)
    sftp = paramiko.SFTPClient.from_transport(t)
    sftp.put(Locdir, Rmtdir)   
    t.close()
 
def read_file():
    global list
    list=[]
    with open('userinfo.txt','rb') as f:
        for line in f:
            list.append(line)
            print list
"""
    mysql = MYSQL(host="localhost",port=3306,user="root",pwd="",db="Automating")
    host = mysql.ExecQuery("select IP,port,user from A_hosts_link ")
    for i in host:
	a,b,c = i[u'IP'], i[u'port'],i['user']
	print a,b,c
"""
"""
	#print a
	#list.append(a)
	#print list
	#map=dict([(v,k) for k,v in i.iteritems()])
"""
"""
	for key in map.keys():
		#print key,":",map[key]
		print key
		list.append(key)
"""
		#print list
"""
    with open('userinfo.txt','rb') as f:
        for line in f:
            list.append(line)
            print list
"""
 
def print_ip():
    global dic
    dic={}
    for i in range(len(list)):
	print i
        lip=list[i].split()[0]
        dic[i]=list[i]
	print dic
        print '【%d】  %s'%(i,lip)
     
def judge():
    global IPList
    IPList=[]
    while True:
        inp=raw_input('\033[34;1m请输入序号选择需要上传的主机,输入ok执行：\033[0m').strip()
        if inp.isdigit() and int(inp) in dic.keys():
            IPList.append(int(inp))
        elif inp == 'ok':
            create_process()
            break
        elif inp == 'exit':
            sys.exit()
        else:
            print '\033[31;1m输入错误,请重新输入\033[0m'
                    
def create_process():
    pool=Pool(processes=4)
    IPListyz=tuple(set(IPList))
    print IPListyz
    while True:    
        Locdir=raw_input('请输入本地文件路径：')
        if os.path.exists(Locdir):
            break
        else:
            print '\033[33;1m本地文件不存在,请重新输入!\033[0m'
    Rmtdir=raw_input('\033[34;1m请输入远程文件路径：\033[0m')
    for i in IPListyz:
        IP=dic[i].split()[0]
        Port=dic[i].split()[1]
        User=dic[i].split()[2]
        print IP
        pool.apply_async(sftp_put,(IP,int(Port),User,Locdir,Rmtdir,))
    pool.close()
    pool.join()
     
if __name__ == '__main__':
    read_file()
    print_ip()
    judge()
    print '\033[33;1m上传成功\033[0m'