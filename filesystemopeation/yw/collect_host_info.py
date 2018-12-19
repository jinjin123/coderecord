#!/usr/bin/python
#-*- coding:UTF-8 -*-
import os
import sys
import commands
import json
import paramiko
from mysql import *
reload(sys) 
sys.setdefaultencoding('utf8')

(status, output) = commands.getstatusoutput('ansible all -m setup --tree /root/hosts -f 10')
def rename_file(path):
        for file in os.listdir(path):
                if os.path.isfile(os.path.join(path,file)) == True:
                        if file.find ('.json') < 0:
                                newname = file + '.json'
                                os.rename(os.path.join(path,file),os.path.join(path,newname))
                               # print file,'ok'
                        else:
                                continue
                else:
                        continue

home_dir = '/root/yw'
file_object = open('%s/ziyuan.txt' %home_dir ,'a')
#file_object.write("rename_file('/root/hosts')")
#print rename_file('/root/hosts') 

if ~status:
        (status,output) = commands.getstatusoutput('ls /root/hosts > /root/host_list')

if ~status:
        mysql = MYSQL(host="localhost",port=3306,user="root",pwd="",db="Automating")

flag = mysql.ExecQuery("show tables like 'Auto_hosts'")

if flag :
        pass
else:
        create_hosts_table = "CREATE TABLE Auto_hosts \
                 (host_id int not null auto_increment PRIMARY KEY,\
                 IP  CHAR(20)  NOT NULL, \
                 hostname  CHAR(50), \
                 mac CHAR(30), \
                 system CHAR(20), \
                 memory CHAR(20), \
                 disk CHAR(20), \
                 kernel CHAR(30), \
                 cpu_info CHAR(100), \
                 cores CHAR(20))" 
        mysql.ExecQuery(create_hosts_table)

file = open("/root/host_list","r")
if file:
        for line in file:
                fact = line.strip('\n')
                #print fact 打印资产信息列表
                f = open('/root/yw/ziyuan.txt','a')	
                f.write('%s ' %fact)
                file_fact = open("/root/hosts/"+fact,"r")
                if file_fact:
                          data = json.loads(file_fact.read())
                          hostname = data['ansible_facts']['ansible_hostname']
                          IP = data['ansible_facts']['ansible_default_ipv4']['address']
                          mac = data['ansible_facts']['ansible_default_ipv4']['macaddress']
                          memory = str(data['ansible_facts']['ansible_memtotal_mb']/1000)+'G'
                          disk = data['ansible_facts']['ansible_devices']['vda']['size']
                          system = data['ansible_facts']['ansible_distribution']+data['ansible_facts']['ansible_distribution_version']+data['ansible_facts']['ansible_architecture']
                          kernel = data['ansible_facts']['ansible_kernel']
                          cpu_info = data['ansible_facts']['ansible_processor'][1]
                          cores = data['ansible_facts']['ansible_processor_cores']+data['ansible_facts']['ansible_processor_count']
                          f.write('%s %s %s %s %s %s %s %s %s ' %(hostname,system,kernel,IP,mac,cpu_info,cores,memory,disk))
                check_host = "select * from Auto_hosts where IP = '%s' " % (IP)
                mysql = MYSQL(host="localhost",port=3306,user="root",pwd="",db="Automating")
                flag = mysql.ExecQuery(check_host)
                #print (flag,type(flag)) 打印列表信息
                if flag:
                         sql = "update Auto_hosts set IP = '%s',hostname = '%s',mac = '%s',memory = '%s',disk = '%s',\
                         system = '%s',kernel = '%s', cpu_info = '%s',cores = '%s' where IP = '%s' " % \
                         (IP,hostname,mac,memory,disk,system,kernel,cpu_info,cores,IP)
                else: 
                         sql = "insert into Auto_hosts (IP,hostname,mac,system,\
                         kernel,cpu_info,cores,memory,disk) \
                         values ('%s','%s','%s','%s','%s','%s','%s','%s' ,'%s') "\
                         % (IP,hostname,mac,system,kernel,cpu_info,cores,memory,disk)

                try:
                       mysql.ExecNonQuery(sql)
                       f.write(" '%s' update successfully !\r" %(hostname))
                       f.close()
                       #print (" '%s' update successfully !") % (hostname)
                except:
                         print 'Something is wrong !!! '

                file_fact.close

