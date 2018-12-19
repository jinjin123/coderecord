#!/usr/bin/env python
#coding=utf-8
import sys
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
import json,codecs
import os,re,time,os.path
import pymongo
from time import sleep, time
from pymongo import MongoClient


from tornado.options import define, options

define("port", default=8888, help="run on the given port", type=int)

class BaseHandler(tornado.web.RequestHandler): 
            def get_current_user(self):
                return  self.get_secure_cookie("user")
	
class HomeHandler(BaseHandler):
            def get(self):
                self.render("index.html")

class HostdelHandler(BaseHandler):
            def post(self):
                port = int(self.get_argument("port"))
                client = MongoClient(os.environ['MONGO_PORT_27017_TCP_ADDR'], 27017)
                #client = MongoClient('localhost', 27017)
                db = client['local']
                db.machinelist.remove({"port":port})
                self.redirect("/host_cmd")

class HostupHandler(BaseHandler):
         def post(self):
                port = int(self.get_argument("port"))
                store = self.get_argument("store")
                client = MongoClient(os.environ['MONGO_PORT_27017_TCP_ADDR'], 27017)
                #client = MongoClient('localhost', 27017)
                db = client['local']
                db.machinelist.update({"port": {'$eq' : port}},{'$set':{"store_id":store}},upsert=False,multi=True)
                self.redirect("/host_cmd")
		

class HostcmdHandler(BaseHandler):
          def get(self):
                client = MongoClient(os.environ['MONGO_PORT_27017_TCP_ADDR'], 27017)
                #client = MongoClient('localhost', 27017)
                db = client['local']
                data = db.machinelist.find()
                self.render("host_cmd.html",**{"dataselect":data})
			
          def  post(self):
                host = self.get_argument("host")
                client = MongoClient(os.environ['MONGO_PORT_27017_TCP_ADDR'], 27017)
                #client = MongoClient('localhost', 27017)
                db = client['local']
                data = db.machinelist.find({"store_id":{'$regex':host}})
                self.render("host_cmd.html",**{"dataselect":data})

class HostlistHandler(BaseHandler):
          def get(self):
                client = MongoClient(os.environ['MONGO_PORT_27017_TCP_ADDR'], 27017)
                #client = MongoClient('localhost', 27017)
                db = client['local']
                data = db.weibo.find()
                self.render("host_list.html",**{"dataselect":data})
			
          def  post(self):
                host = self.get_argument("host")
                client = MongoClient(os.environ['MONGO_PORT_27017_TCP_ADDR'], 27017)
                #client = MongoClient('localhost', 27017)
                db = client['local']
                data = db.weibo.find({"dining_id":{'$regex':host}})
                self.render("host_list.html",**{"dataselect":data})

class MainHandler(BaseHandler):
         def get(self):
                self.render("index.html")
	
settings = {
        "cookie_secret":"81oETzKXQAGaYdkL5gEmGeJJFuYh7EQnpZXdTP1o/Vo=",
        "login_url":"/login",
        "template_path":os.path.join(os.path.dirname(__file__),"templates"),
        "static_path":os.path.join(os.path.dirname(__file__),"static"),
        "debug": True,
        "xsrf_cookie" : True,
        "gzip" : True
        }


def main():
    tornado.options.parse_command_line()
    application = tornado.web.Application([
        (r"/", MainHandler),
        (r"/home", HomeHandler),
        (r"/update", HostupHandler),
        (r"/host_cmd", HostcmdHandler),
        (r"/host_del", HostdelHandler),
        (r"/host_list", HostlistHandler),
    ],**settings)
    http_server = tornado.httpserver.HTTPServer(application)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()


if __name__ == "__main__":
    main()
