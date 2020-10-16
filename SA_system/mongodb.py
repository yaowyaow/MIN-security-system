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


from kafka import KafkaProducer
from kafka import KafkaConsumer
import json
from kafka.errors import KafkaError

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
		self.producer = KafkaProducer(bootstrap_servers=['localhost:9092'])

		self.db_connect()
		self.event_logger = event_Logger(__name__).get_event_log()
                self.logger = Logger(__name__).get_log()
		

		#self.event_logger.critical("detect some attack event: ")
		return

        def kafka_insert(self, data):

                # Asynchronous by default
                print "start kafka"
                try:
                        json_data = json.dumps(data)
                        self.producer.send('MIN-packet', json_data)
                except Exception as e:
                        print e
                print "kafka insert success"


	def db_connect(self):
		try:
			self.db_conn = MongoClient()
			#mongodb collection
			#exec(str("print 'test'"))
			exec("self.db = " + str(self.db_conn) + "." + str(self.db_database))
			print self.db
			self.db.authenticate("pkusz", "pkusz")
			exec("self.collection = " + "self.db" + "." + str(self.db_collection))
			print self.collection
			self.db_connect_status = str(self.db_conn).split(" ")[-1][:-1]
			print "\n=====Connected to MONGODB =====\n" + self.db_connect_status + "\n"
			self.mon = self.db[str(self.db_collection)]
		except:
			print "MongoDB connect failed"

	def db_insert(self, data_dict):
		try:
			print str(self.collection)
			print self.mon.insert(data_dict)
			print self.collection, " \n insert succeed\n"
		except Exception as e:
			print "\nDB insert failed!\n"
			print "\n", e
			print type(data_dict)
			print "\ndata :\n",repr(data_dict)

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

		access = {}
		count = 0
		# use queue to insert
		#self.event_logger.critical("detect some attack event2: ")
		while True:
			if not data_queue.empty():
				#time.sleep(0.005)
				data = data_queue.get()
				#self.event_logger.critical("detect some attack event: ")
				try:
					#需要进行Unicode解码
					NDN_packet = data["data"]
					data["data"] = data["data"].decode("unicode_escape")
					if NDN_packet[0] == '\x05': #兴趣包标志位
						data["packet_type"] = "interest_packet"
					elif NDN_packet[0] == '\x06': #数据包标志位
						data["packet_type"] = "data_packet"
					else:
						data["packet_type"] = "data_packt"
					
					print "packet_type success"                        

					#提取前缀请求, repr防止packet转义，re.I忽视大小写
					#request_re = re.search(r'(\\x08\\x([0-9,a-f]){2}([0-9,a-z])*)+',repr(NDN_packet), re.I).group()
					request_re = re.search(r'(\\x08\\x([0-9,a-f]){2}([^\\])*)+',repr(NDN_packet), re.I).group()
					request = re.sub(r'\\x08\\x([0-9,a-f]){2}', '/', request_re)
					data["request"] = request
					print "request success"
					#提取请求信息
					#message = re.sub(r'[(\n)|\s]*','',NDN_packet)
					#message = re.search(r'\{((\n)*?([\:\w\"\s\,])*?)*?(\".*?\")*?\}',(message), re.I).group()
					message_dict = {}
					try:
						message = re.sub(r'[(\n)|\s]*','',NDN_packet)
                                        	message = re.search(r'\{((\n)*?([\:\w\"\s\,])*?)*?(\".*?\")*?\}',(message), re.I).group()
						message_dict = eval(message)
						data["survice"] = 1
					except:
						print "survice not match the json format"
						data["survice"] = 0
						pass
							#data_dict["message"] = message_dict
					#提取身份信息和访问接口信息
					if 'username' in message_dict:
						data["username"] = message_dict["username"]
					else:
						data["username"] = "null"
						#raise    #跳入except    
					if 'command' in message_dict:
						data["command"] = message_dict["command"]
					else:
						data["command"] = "null" 
						#raise
					if 'uuid' in message_dict:
						data["uuid"] = message_dict["uuid"] 
					else:
						data["uuid"] = "null"
					print "survey extract success"
					print data

					self.kafka_insert(data)
					self.db_insert(data)



				except:
					pass
					#print "analyze fail(mongo.py)"
					#print data

				'''count += 1

				#对数据进行检测分析
				if is_analyze:
				  #data = Filter_module(data).match()
				  try:
					if count < 1000:
						print data["src_ip"], data["dport"]
						if "src_ip" in data and "dport" in data:
						#if True:
							if data["src_ip"] not in access: 
								access[data["src_ip"]] = [1]
								access[data["src_ip"]].append(data["dport"])
							else:   
								access[data["src_ip"]][0] += 1
								if data["dport"] not in access[data["src_ip"]]:
									access[data["src_ip"]].append(data["dport"])
					else:
						for each in access.items():
							#when ip_count > 10 and dport_count > 4
							if each[1][0] > 10 and len(each[1]) > 1:
							#if True:
								#maybe evil behavior
								self.logger.critical("detect some attack event: (maybe someone is scanning your port)"+ str(each[0]) + str(each[1]))
								self.event_logger.critical("detect some attack event: (maybe someone is scanning your port)"+ str(each[0]) + str(each[1]))

								
						access = {}
						count = 0
				  except:
					print "---------------------------"
					
					

				#if 'danger' in data.keys():
				self.db_insert(data)'''
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
	mongDB.kafka_insert("first test")
	
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

