#!/usr/bin/python
#-*- coding:utf8 -*-
import os,sys,json
reload(sys)
sys.setdefaultencoding("utf-8")
def send_status():
        server_status={"10.0.0.1":"red","10.0.0.2":"green","10.0.0.3":"red"}
        server_info={"10.0.0.1":"服务器:root@10.0.0.1 </br>消息:服务器没响应"}
        print json.dumps(server_status,encoding="UTF-8",ensure_ascii=False)
        print json.dumps(server_info,encoding="UTF-8",ensure_ascii=False)
if  __name__=='__main__':
        send_status()

