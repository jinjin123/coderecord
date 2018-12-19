#!/usr/bin/python
#-*- coding:UTF-8 -*-
import os
import sys
import commands
import json
from mysql import *

(status, output) = commands.getstatusoutput('ansible all -m setup --tree /root/hosts')
def rename_file(path):
        for file in os.listdir(path):
                if os.path.isfile(os.path.join(path,file)) == True:
                        if file.find ('.json') < 0:
                                newname = file + '.json'
                                os.rename(os.path.join(path,file),os.path.join(path,newname))
                                print file,'ok'
                        else:
                                continue
                else:
                        continue

print rename_file('/root/hosts')

if ~status:
        (status,output) = commands.getstatusoutput('ls /root/hosts > /root/host_list')

if ~status:
        mysql = MYSQL(host="localhost",port=3306,user="root",pwd="",db="Automating")

flag = mysql.ExecQuery("show tables like 'hosts'")

if flag :
        pass
else:
        create_hosts_table = "CREATE TABLE hosts \
                 (IP  CHAR(20) PRIMARY KEY NOT NULL, \
                 hostname  CHAR(50), \
                 mac CHAR(30), \
                 distribution CHAR(20), \
                 kernel CHAR(30), \
                 cpu_info CHAR(100), \
                 cores CHAR(20))" 
        mysql.ExecQuery(create_hosts_table)

file = open("/root/host_list","r")
if file:
        for line in file:
                fact = line.strip('\n')
                print fact

                file_fact = open("/root/hosts/"+fact,"r")
                if file_fact:
                        data = json.loads(file_fact.read())
                        hostname = data['ansible_facts']['ansible_hostname']
                        IP = data['ansible_facts']['ansible_default_ipv4']['address']
                        mac = data['ansible_facts']['ansible_default_ipv4']['macaddress']
                        distribution = data['ansible_facts']['ansible_distribution']+data['ansible_facts']['ansible_distribution_version']+data['ansible_facts']['ansible_architecture']
                        kernel = data['ansible_facts']['ansible_kernel']
                        cpu_info = data['ansible_facts']['ansible_processor'][1]
                        cores = data['ansible_facts']['ansible_processor_cores']+data['ansible_facts']['ansible_processor_count']
                        print hostname,distribution,kernel,IP,mac,cpu_info,cores
		check_host = "select * from hosts where IP = '%s' " % (IP)
		mysql = MYSQL(host="localhost",port=3306,user="root",pwd="",db="Automating")
		flag = mysql.ExecQuery(check_host)
                print (flag,type(flag))
		if flag :
                        sql = "update hosts set IP = '%s',hostname = '%s',mac = '%s',\
                        distribution = '%s',kernel = '%s', cpu_info = '%s',cores = '%s' where IP = '%s' " % \
                        (IP,hostname,mac,distribution,kernel,cpu_info,cores,IP)
		else:
                        sql = "insert into hosts (IP,hostname,mac,distribution,\
                        kernel,cpu_info,cores) \
                        values ('%s','%s','%s','%s','%s','%s','%s') "\
                         % (IP,hostname,mac,distribution,kernel,cpu_info,cores)
                try:
                        mysql.ExecNonQuery(sql)
                        print (" '%s' update successfully !") % (hostname)
                except:
                        print 'Something is wrong !!! '

                file_fact.close

