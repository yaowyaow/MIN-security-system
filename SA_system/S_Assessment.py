#coding=utf-8
import os
import pymongo
import time
from time import gmtime,strftime
import threading
import SA_predict

try:
	import pymysql
except:
	try:
		command_to_execute = "pip2 install pymysql"
		os.system(command_to_execute)
	except:
		print "can't install pymysql"
		sys.exit(1)
	import pymysql


class S_Assessment(object):
	
	def __init__(self):
		self.db = pymysql.connect(host="localhost", user="root", password="root", port=3306)
		self.cursor = self.db.cursor()
		self.cursor.execute("use ossec;")

	#参数是时间
	def read_data(self, mins):
		#时间区间,5mins
		t = time.time() - mins*60
		sql = "select rule_id,level from alert where timestamp >= " + str(t) + ";"
		try:
			print "==========\nsql: ",sql,"============"
			self.db = pymysql.connect(host="localhost", user="root", password="root", port=3306)
                	self.cursor = self.db.cursor()
                	self.cursor.execute("use ossec;")
			self.cursor.execute(sql)
		except Exception as e:
			print e
		row = self.cursor.fetchone()
		logs = []
		while row:
			#row is tuple, row[2]:rule_id, row[3]:level, row[4]:timestamp, row[6]:src_ip, row[11]:user, row[12]:full_log
			logs.append(row)
			row = self.cursor.fetchone()
		print "logs: ",logs
		if logs == []:
			return 0;
		#else:
		#	print logs
		freq = {}
		level = {}
		for each in logs:
			if each[0] not in freq:
				freq[each[0]] = 1
				level[each[0]] = each[1]
			else:
				freq[each[0]] += 1
		#时间向量,只取时-分-秒
		t_now = strftime("%H:%M:%S")
		if t_now >= "0" and t_now < "9": #24:00 - 9:00
			t_vector = 1
		elif t_now >= "9" and t_now < "18": #9:00 - 18:00
			t_vector = 3
		else:
			t_vector = 2

		#计算态势值
		result = 0
		for k,v in freq.items():
			#将10修改为3
			result += v*(pow(3, level[k]))
		result *= t_vector
		#print "*************************result: ",result
		return result	

#主机态势威胁值
	def run(self, mins):
		print "is running"
		client = pymongo.MongoClient("mongodb://localhost:27017/")
		db = client['Situation_Awareness']
		db.authenticate("pkusz", "pkusz")
		collection_name = 'SA_host_value'
		collection = db[collection_name]
		while True:
			result = self.read_data(mins)
			ans = {"value":result, "time":time.strftime("%Y-%m-%d %H:%M:%S")}
			collection.insert_one(ans)
			SA_predict.start2()
			time.sleep(mins*60)

	def predict_value(self, seconds):
		while True:
			SA_predict.start()
			time.sleep(seconds)

	def predict_host_value(self, mins):
		while True:
			SA_predict.start2()
			time.sleep(mins*60)
		

if __name__ == "__main__":
	test = S_Assessment()
	test.run(3)
	'''
	t_1 = threading.Thread(target=test.run, args=(3,))
	t_2 = threading.Thread(target=test.predict_value, args=(3,))
	t_3 = threading.Thread(target=test.predict_host_value, args=(3,))
	t_2.setDaemon(True)
	t_3.setDaemon(True)
	t_1.start()
	t_2.start()
	t_3.start()
	'''
			
		




				
