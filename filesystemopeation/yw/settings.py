#coding=utf-8
import pymysql
from pymongo import MongoClient
client = MongoClient('localhost',27017)
db = client['bor']

