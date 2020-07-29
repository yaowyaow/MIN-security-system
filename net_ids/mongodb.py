#!/usr/bin/python
# encoding: utf-8
# -*- coding: utf8 -*-


import os
import sys
import threading
import Queue
import time
import datetime
import argparse
from Filter_module import *

try:
    import pymongo
    from pymongo import MongoClient
except ImportError:
    try:
        command_to_execute = "pip install pymongo"
        os.system(command_to_execute)
    except OSError:
        print "Can NOT install pymongo, Aborted!"
        sys.exit(1)
    import pymongo
    from pymongo import MongoClient

class mongoOperate():
	
	#initialization
	def __init__(self, db_database, db_collection):
		#time.sleep(1)
		self.db_database = db_database
		self.db_collection = db_collection
		self.db = False
		self.collection = False
		self.db_connect()
		return

	def db_connect(self):
		try:
			self.db_conn = MongoClient()
			#mongodb collection
			#exec(str("print 'test'"))
			exec("self.db = " + str(self.db_conn) + "." + str(self.db_database))
			print self.db
			exec("self.collection = " + "self.db" + "." + str(self.db_collection))
			print self.collection
			self.db_connect_status = str(self.db_conn).split(" ")[-1][:-1]
			print "\n=====Connected to MONGODB =====\n" + self.db_connect_status + "\n"
		except:
			print "MongoDB connect failed"

	def db_insert(self, data_dict):
		try:
			self.collection.insert(data_dict)
			#print self.collection, " \n insert succeed\n"
		except:
			print "\nDB insert failed!\n"
			print "data :\n",repr(data_dict)

	def db_read(self, comand):
		try:
			if command == "all":
				result = self.collection.find()
			
			for each in result:
				print each
			#根据命令进行查找
			return result
		except:
			print "\n search error\n"
	
	def run(self, data_queue, is_analyze):
		#self.db_connect()
		threading._sleep(1)

		# use queue to insert
		while True:
			if not data_queue.empty():
				time.sleep(0.5)
				data = data_queue.get()
				#对数据进行检测分析
				if is_analyze:
					data = Filter_module(data).match()
				#if 'danger' in data.keys():
				self.db_insert(data)
		#	else:
		#		break
			#	print "insert success\n"

	def get_count(self):
		if self.collection:	
			return self.collection.count()
		else:
			return -1
	
	def get_database(self, order, limit_count):
		if self.collection:
			#注意这里python操作db排序的时候不能用字典，要用列表+元组
			a =  self.collection.find().sort([("_id",order)]).limit(limit_count)
			if limit_count < 20 and limit_count != 0:
				for each in a:
					print each,"\n"
			return a
			
		else:
			return -1

	def get_message(self, sql_dict_str, limit_set):
		if self.collection:
			sql_dict = eval(sql_dict_str)
			a =  self.collection.find(sql_dict).sort([("_id",args.order)]).limit(limit_set)
			print a.count()
			if limit_set > 0 and limit_set < 20:
				for each in a:
					print each
			return a
		else:
			return -1
	def get_user_frequency(self, username, mins, days_set, limit_set):
		if self.collection:
			now_time = datetime.datetime.now()
			if days_set == 0 :
				previous_time = (now_time+datetime.timedelta(minutes=-mins)).strftime("%Y-%m-%d %H:%M:%S")
			elif days_set > 0 :
				previous_time = (now_time+datetime.timedelta(days=-days_set)).strftime("%Y-%m-%d %H:%M:%S")
			else:
				return -1

			result = self.collection.find({"username":username, "Time":{'$gte':previous_time}}).sort([("_id",args.order)]).limit(limit_set)
		
			if limit_set < 20 and limit_set > 0:
				for each in result:
					print each,"\n"	
			return result
	def get_users(self):
		users = self.collection.distinct("username")
		for each in users:
			print each
		return users


	def get_special_key_values(self, key):
		self.collection.find({key:{"$exists":true}},{ key:1, "_id":0})
		return 1

#usage:
#mongodb = mongoOperate("packet_flow", "packet_flow")
#mongodb.run(data_queue)

if __name__ == "__main__":
	print "only display at most 20 messages if limit param is set"
	parser = argparse.ArgumentParser()
	parser.add_argument('-f', '--find', action='store_true', help="find under demands, need -e,-l")
	parser.add_argument('-g', '--get_frequency', action='store_true', help="view the user's frequency, need -u, -m, -d, -l")
	parser.add_argument('-a', '--all', action='store_true', help="get all messages, need -o, -l")
	parser.add_argument('-us', '--users', action='store_true', help="get all users")

	parser.add_argument('-c', '--count', action='store_true', help="the count of the whole db")
	

	parser.add_argument('-o', '--order', default=1, help="the order of results",type=int)
	parser.add_argument('-m', '--minutes', default=1, help="minutes ago -> now set",type=int)
	parser.add_argument('-l', '--limit', default=0, help="limit the displayed count",type=int)
	parser.add_argument('-u', '--username', default='', help="set username", type=str)
	parser.add_argument('-d', '--days', default=0,help="days ago -> now ",type=int)
	parser.add_argument('-e', '--demand',default="", help="search conditions", type=str)
	args = parser.parse_args()

	mongDB = mongoOperate("packet_flow", "packet_flow")
	mongDB.db_connect()
	
        if args.count:
                print "the count :\n " ,mongDB.get_count()

	if args.all:
		print "data : \n" , mongDB.get_database(args.order, args.limit)

	if args.get_frequency:
		print "result : \n" , mongDB.get_user_frequency(args.username, args.minutes, args.days, args.limit)

	if args.find:
		print "find :\n" , mongDB.get_message(args.demand,args.limit)
	
	if args.users:
		print "users:\n", mongDB.get_users()


	#print mongDB.get_user_frequency("xxx_test", 600)	

