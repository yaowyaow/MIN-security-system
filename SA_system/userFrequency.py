#!/usr/bin/env python
# coding=utf-8
import time
from  pymongo import * 



def recordFrequency(db, conn, interval):
	while(True):
		#get users
		userList = conn.distinct("username")

		oldDate = time.strftime('%Y-%m-%d %H:%M:%S')
		time.sleep(interval)
		nowDate = time.strftime('%Y-%m-%d %H:%M:%S')
		for user in userList:
			data = {}
			data["Time"] = nowDate
			data["username"] = user
			data["frequency"] = conn.find({"username":user, "Time":{ "$gte" : oldDate, "$lt" : nowDate}}).count()
			data["commands"] = conn.distinct("command", {"username":user, "Time":{ "$gte" : oldDate, "$lt" : nowDate}})
			db.userFrequency.insert(data)
			print data

def run():
	db = MongoClient().packet_flow
	db.authenticate("pkusz", "pkusz")
	conn = db.packet_flow
	recordFrequency(db, conn, 120)


if __name__ == "__main__":
	run()
