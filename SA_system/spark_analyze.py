#encoding=utf8
from pyspark import SparkContext
from pyspark import SparkConf
from pyspark.streaming import StreamingContext
from pyspark.streaming.kafka import *
import kafka
import json
import pymongo
from pymongo import MongoClient
import threading
from urlDetect.urlDetect import *

import json
import csv
import sys


import os
os.environ['PYSPARK_SUBMIT_ARGS'] = '--jars spark-streaming-kafka-0-8-assembly_2.11-2.4.6.jar pyspark-shell'

from flowDetect.flowDetect import *
from utils import *
from time import gmtime,strftime
import time
import psutil

import SA_predict

try:
	import requests
except:
	os.system("pip2 install requests -i https://pypi.tuna.tsinghua.edu.cn/simple")
	import requests
#import org.apache.spark.rdd.RDD

counter=0
offsets = []
def out_put(m):
    print(m)
def store_offset(rdd):
    global offsets
    offsets = rdd.offsetRanges()
    return rdd
 
def print_offset(rdd):
    for o in offsets:
        print ("%s %s %s %s %s" % (o.topic, o.partition, o.fromOffset, o.untilOffset,o.untilOffset-o.fromOffset))
 
''' 
config = SparkConf()
#scontext = SparkContext(appName='kafka_pyspark_test',)
scontext = SparkContext("local[2]", "kafka_pyspark_test")
stream_context = StreamingContext(scontext,5)
msg_stream = KafkaUtils.createDirectStream(stream_context,['test',],kafkaParams={"metadata.broker.list": "127.0.0.1:9092,"})
#result = msg_stream.map(lambda x :json.loads(x).keys()).reduce(out_put)
#msg_stream.transform(store_offset,).foreachRDD(print_offset)
#result.pprint()

targets = msg_stream.map(lambda msg_stream: msg_stream[1])
'''

json_values = []


freq_dict = {}
def mapper(record):
    record = json.loads(record)
    res = {}
    res["Source IP"] = record.get("ip_src")
    if record.get("ip_src") == "121.15.171.82":
	with open("test_lgx.txt","a") as f:
		f.write("success")
		f.close()
    res['Dest IP'] = record.get('ip_dst')
    res['Transport Layer'] = record.get('ip_proto')
    res['Source Port'] = record.get('port_src')
    res['Dest Port']= record.get('port_dst')
    #res['Attack Length'] = record.get('bytes')
    res['Attack Length'] = 0
    res['Packet Length'] = record.get('bytes')
    res['timestamp'] = record.get('timestamp_start')
    if res["Source IP"] not in freq_dict:
        freq_dict[res["Source IP"]] = 1
        res["frequency"] = 1
    else:
        freq_dict[res["Source IP"]] += 1
        res["frequency"] = freq_dict[res["Source IP"]] + 1
    res = json.dumps(res)
    #result = ddos_detect(json.dumps(res))
    '''if result["Hostile_Packets_Detected"] != 0:
	#write to the log file
    #if hostile != 0:
        #evil event log
        event_lg.debug(data)
    else:
#       Logger("flow_normal_log").get_log().critical(data)
        lg.debug(data)
'''

    #write(res)
    return res




from kafka import KafkaProducer
#持久化，输出到新的kafka topic

producer = KafkaProducer(
    bootstrap_servers=['127.0.0.1:9092'],
    linger_ms=1000,
    batch_size=1000,
)


count = 1
def nums_count(data):
    global count
    count += 1
    print(count)



def sendTest1(message):
    records = message.collect()
    with open("test_data.json", "a") as json_file:
        for json_str in records:
            json_file.write(json_str + '\n')
        json_file.close()


def sendTest(message):
    records = message.collect()
    print("=========================",type(records))
    #ddos_result = ddos_detect(records)
    try:
        ddos_result = ddos_detect(records)
	if ddos_result["Hostile_Packets_Detected"] != '0':
		event_data = json.loads(ddos_result["Hostile_Packets_Info"])
		event_data[0]["event"] = "DDoS"
		print event_data
		sendMongoDB(event_data)
	pass
    except Exception as e:
	print "ddos:\n",e
        pass
    try:
	#'''
        nmap_result = nmap_detect(records)
	if nmap_result["Hostile_Packets_Detected"] != '0':
		#print '默认接收为json格式，转换'
		event_data = json.loads(nmap_result["Hostile_Packets_Info"])
		for each in event_data:
			each["event"] = "Scan" 
		print event_data
		sendMongoDB(event_data)
	#'''
	pass
    except Exception as e:
	print "nmap:\n",e
        #pass
    try:
        S_Assess(nmap_result["Hostile_Packets_Detected"], ddos_result["Hostile_Packets_Detected"])
	pass
	#S_Assess(0,0)
    except Exception as e:
	print "S_Assess:",e
	#print ddos_result
        pass

#查询对应城市信息后插入MongoDB
def sendMongoDB(records):
	record = records[0]
	ip = record["Source IP"]
	url = 'http://api.ipstack.com/{}?access_key=1bdea4d0bf1c3bf35c4ba9456a357ce3'
	message = requests.get(url.format(ip))
	message = message.json()
	if message != None:
		new_record = {}
		new_record["srcIp"] = ip
		new_record["srcPort"] = record["Source Port"]
		new_record["type"] = record["event"]
		new_record["destIp"] = record["Dest IP"]
		new_record["destName"] = "PKUSZ"
		new_record["destLocY"] = 22.55516
		new_record["destLocX"] = 114.053879
		new_record["time"] = time.strftime("%Y-%m-%d %H:%M:%S")
		new_record["srcName"] = str(message['city'])
		new_record["srcLocY"] = message['latitude']
		new_record["srcLocX"] = message['longitude']

		#插入SA_event表
		global db
		db_col = db["SA_event"]
		db_col.insert_one(new_record)
	
	
	'''
	for each in records:
		ip = each["Source ip"]
		message = geolite2.lookup(ip)
		each
	'''
	
		
	

#最大带宽
MAX_SPEED = 65
#态势评估
def S_Assess(nmap, ddos):
    if nmap!='0' or ddos!='0':
	    #定权值
	    nmap = 1 if nmap>"0" else 0
	    ddos = 2 if ddos>"0" else 0
	    #时间向量
	    t_now = strftime("%H:%M:%S")
	    if t_now >= "0" and t_now < "9": #24:00 - 9:00
		t_vector = 1
	    elif t_now < "18": #9:00 - 18:00
		t_vector = 3
	    else:
		t_vector = 2
	    #带宽占用比
	    speed_o = list(psutil.net_io_counters())
	    time.sleep(1)
	    speed_n = list(psutil.net_io_counters())
	    speed = float(speed_n[1] - speed_o[1])/(1024*1024)
	    speed_percent = speed/MAX_SPEED
	    #cpu占用比
	    cpu = psutil.cpu_percent(None)/100
	    #cpu和bindwidth中和
	    quality = (speed_percent + cpu)
	    #求态势值
	    result = t_vector*(pow(10,nmap) + pow(10,ddos)*quality)
	    #with open("test_value.txt", "a") as file_object:
	    #	file_object.write("1\n")
	#	file_object.write("result: "+str(result) + "time_vector: "+str(t_vector) + "nmap: "+ str(nmap) + " ddos: "+ str(ddos)+" quality: "+ str(quality)+"\n")
	#	file_object.write("pow(10,ddos)*quality"+str(pow(10,ddos)*quality)+"\n")
		#file_object.close()
    else:
	    result = 0
    #sendMongoDB
    global collection
    ans = {"value":result, "time":strftime("%Y-%m-%d %H:%M:%S")}
    collection.insert_one(ans)
    SA_predict.start()

    

def min_detect(records):
    message = records.collect()
    if len(message) > 0:
	result = detectBatch(message)
    else:
	result = []
    #result = message
    print "result: ",result
    
    for each in result:
	each = eval(each)
	server_id = "1"
	rule_id = "001"
	level = 6
	timestamp = time.time()
	location_id = "2"
	src_ip = each["src_ip"]
	dst_ip = each["dst_ip"]
	src_port = each["sport"]
	dst_port = each["dport"]
	alertid = "0"
	user = each["username"]
	full_log = "request abnormal, maybe malicious request" + each["request"]
	sql = '''insert into alert(server_id, rule_id, level, timestamp, location_id, src_ip, dst_ip, src_port, dst_port, alertid, user, full_log) value(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'''
	cursor.execute(sql, (server_id, rule_id, level, timestamp, location_id, src_ip, dst_ip, src_port, dst_port, alertid, user, full_log))
	sql_db.commit()
	#send to mongodb
	global db_min
	each['danger'] = full_log
	db_min['event_log'].insert_one(each)
	print "mongo insert success,(event_log)min-packet"
	
    
    

# event_lg = event_Logger("flow_log").get_event_log()
# lg = Logger("flow_normal_log").get_log()
try:
	client = pymongo.MongoClient("mongodb://localhost:27017/")
	db = client['Situation_Awareness']
	db_min = client['packet_flow']
	collection_name = 'SA_value'
	collection = db[collection_name]
except Exception as e:
	print e, "\n mongodb init failed"

try:
	import pymysql
	sql_db = pymysql.connect(host="localhost", user="root", password="root", port=3306)
	cursor = sql_db.cursor()
	cursor.execute("use ossec;")
except Exception as e:
	print e,"\n mysql init failed"

def run_ip_detect(stream_context):
	'''
	config = SparkConf()
	#scontext = SparkContext(appName='kafka_pyspark_test',)
	scontext = SparkContext("local[2]", "kafka_pyspark_test")
	stream_context = StreamingContext(scontext,5)
	'''
	msg_stream = KafkaUtils.createDirectStream(stream_context,['test',],kafkaParams={"metadata.broker.list": "127.0.0.1:9092,"})
	'''result = msg_stream.map(lambda x :json.loads(x).keys()).reduce(out_put)
	msg_stream.transform(store_offset,).foreachRDD(print_offset)
	result.pprint()
	'''

	targets = msg_stream.map(lambda msg_stream: msg_stream[1])
	process = targets.map(mapper)

	process.pprint()

	#process.map(lambda key:key["ip_src"]).countByValue()
	#process.pprint()
	#process.foreachRDD(sendKafka)
	process.foreachRDD(sendTest)

	#process.foreachRDD(lambda rdd: rdd.foreachPartition(sendMongoDB))
	#msg_stream.saveAsTextFile('out.txt')
	#msg_stream.pprint()
	stream_context.start()
	stream_context.awaitTermination()
	 
def run_min_detect(stream_context):
	#config = SparkConf()
        #scontext = SparkContext(appName='kafka_pyspark_test',)
        #scontext = SparkContext("local[1]", "kafka_pyspark_min-packet")
        #stream_context = StreamingContext(scontext,5)
        msg_stream = KafkaUtils.createDirectStream(stream_context,['MIN-packet',],kafkaParams={"metadata.broker.list": "127.0.0.1:9092,"})
	Targets = msg_stream.map(lambda msg_stream: msg_stream[1])
	Targets.pprint()
	Targets.foreachRDD(min_detect)

	stream_context.start()
	stream_context.awaitTermination()

def exec_ip():
	os.system("python spark_analyze.py 'ip'")

def exec_min():
	os.system("python spark_analyze.py 'min'")


if __name__ == "__main__":
	config = SparkConf()
	scontext = SparkContext("local[2]", "kafka_pyspark_min-packet")
	stream_context = StreamingContext(scontext,3)
	'''
	t_ip = threading.Thread(name="ip detect", target=run_ip_detect, args=(stream_context,))
	t_min = threading.Thread(name="min detect", target=run_ip_detect, args=(stream_context,))
	#t_min.setDaemon(True)
	#t_ip.start()
	t_min.start()
	#time.sleep(3)
	t_ip.start()
	'''
	#sendMongoDB([{"event":"scan","Dest IP":"192.168.3.50","Dest Port":9001.0,"Packet Length":'null',"Source IP":"121.15.171.82","Source Port":51130.0,"Transport Layer":"tcp"},{"Dest IP":"192.168.3.50","Dest Port":8010.0,"Packet Length":'null',"Source IP":"121.15.171.82","Source Port":44958.0,"Transport Layer":"tcp"},{"Dest IP":"192.168.3.50","Dest Port":9002.0,"Packet Length":'null',"Source IP":"121.15.171.82","Source Port":42504.0,"Transport Layer":"tcp"},{"Dest IP":"192.168.3.50","Dest Port":9000.0,"Packet Length":'null',"Source IP":"121.15.171.82","Source Port":50802.0,"Transport Layer":"tcp"}])
	if len(sys.argv[1:]) < 1:
		print "must have a param, 'ip' or 'min'"
		exit()	
	if sys.argv[1] == "ip":
		run_ip_detect(stream_context)
	elif sys.argv[1] == "min":
		run_min_detect(stream_context)
	elif sys.argv[1] == "all":
		t_ip = threading.Thread(target=exec_ip, args=())
		#t_min = threading.Thread(target=exec_min, args=())
		t_ip.start()
		#t_min.start()
		exec_min()
		
	else:
		print "params error"
	#ddos_detect(['sdf'])
