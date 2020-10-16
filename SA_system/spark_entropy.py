#encoding=utf8
import pyspark
from pyspark import SparkContext
from pyspark import SparkConf
from pyspark.streaming import StreamingContext
from pyspark.streaming.kafka import KafkaUtils
from pyspark.sql import *
import kafka
import json
import pymongo
from pymongo import MongoClient
from operator import add

from pyspark.sql import Row


from pyspark.sql.functions import col



import json
import csv


import os
os.environ['PYSPARK_SUBMIT_ARGS'] = '--executor-cores 5 --executor-memory 8g  --jars spark-streaming-kafka-0-8-assembly_2.11-2.4.6.jar pyspark-shell'

#os.environ['PYSPARK_SUBMIT_ARGS'] = '--num-executors 5'

#import org.apache.spark.rdd.RDD

offsets = []
def out_put(m):
    print(m)
def store_offset(rdd):
    global offsets
    offsets = rdd.offsetRanges()
    return rdd
 
def print_offset(rdd):
    for o in offsets:
        print( "%s %s %s %s %s" % (o.topic, o.partition, o.fromOffset, o.untilOffset,o.untilOffset-o.fromOffset))
 
 
config = SparkConf().set("spark.streaming.kafka.maxRatePerPartition", 30000)
scontext = SparkContext(conf=config)
#scontext = SparkContext("local[2]", "kafka_pyspark_test")
stream_context = StreamingContext(scontext,3)
msg_stream = KafkaUtils.createDirectStream(stream_context,['test',],kafkaParams={"metadata.broker.list": "127.0.0.1:9092,"})
'''result = msg_stream.map(lambda x :json.loads(x).keys()).reduce(out_put)
msg_stream.transform(store_offset,).foreachRDD(print_offset)
result.pprint()
'''

targets = msg_stream.map(lambda msg_stream: msg_stream[1])

json_values = []



    
def write(res):
	json_str = json.dumps(res)
	with open("test_data.json", "a") as json_file:
		json_file.write(json_str)

def entropy(data):
	#p = data.map(lambda x:(x,1)).reduceByKey(_+_)
	#print "++++++++++++++++",count,"++++++++++++++++"
	return data.map(lambda key:(key["ip_src"], 1)).reduceByKey(_+_)
		
	#p = data.map(x=>(x,1)).reduceByKey(_+_).map{
      	#	case(value,num)=>num.toDouble/size
    	#}
	#p.map{x=>
	#	-x*(Math.log(x)/Math.log(2))
	#}.sum



freq_dict = {}
def mapper(record):
    record = json.loads(record)
    res = {}
    res["ip_src"] = record.get("ip_src")
    res['ip_dst'] = record.get('ip_dst')
    res['event_type'] = record.get('event_type')
    res['packets'] = record.get('packets')
    res['bytes'] = record.get('bytes')
    res['protocol'] = record.get('ip_proto')
    res['timestamp'] = record.get('timestamp_start')
    res['port_src'] = record.get('port_src')
    res['port_dst'] = record.get('port_dst')
    #frequency
    if res["ip_src"] not in freq_dict:
        freq_dict[res["ip_src"]] = 1
        res["frequency"] = 1
    else:
        freq_dict[res["ip_src"]] += 1
        res["frequency"] = freq_dict[res["ip_src"]] + 1

    '''global count
    global json_values
    count += 1
    if count == 100000:
	json_to_csv(res)	
    else:
	json_values.append(res.values())
	print "================\n",count,"============="
'''
    #write(res)
    return res


def sendMongoDB(partition):
    # 初始化 mongo
    client = pymongo.MongoClient("mongodb://localhost:27017/")
    db = client['kafka-netflow']
    collection_name = 'netflow'
    collection = db[collection_name]
    
    for record in partition:
        collection.insert_one(record)
        
    client.close()


from kafka import KafkaProducer
#持久化，输出到新的kafka topic
producer = KafkaProducer(
    bootstrap_servers=['127.0.0.1:9092'],
    linger_ms=1000,
    batch_size=1000,
)
def sendKafka(message):
    records = message.collect()
    for record in records:
        producer.send('abstracted_topic', str(record).encode())
        producer.flush()


count = scontext.accumulator(0)
def nums_count(data):
	global count
	count += 1
	print( "count: ",count)
	return data

c = count.value
def nums_count2(data):
	global count
	return data, c

#targets.map(nums_count).pprint()

#process = targets.map(mapper)
targets.count().pprint()
#process.pprint()




'''
a = process.map(nums_count)
a.pprint()
print "1111111111111111111111111: ",count.value
#try:
a.persist(pyspark.StorageLevel.MEMORY_AND_DISK_2).count()
a.cache().count()
'''
#except Exception as e:
#	print e
#a.count()
#a.cache()

#process = targets.map(entropy)
#process.pprint()
#process.map(lambda key:(process.count)).pprint()
testc = 100.
#testc = len(process)
#process.map(lambda key:(key["ip_src"], 1)).reduceByKey(add).map(lambda (x,y):(x,float(y)/count)).pprint()
#process.map(lambda key:(key["ip_src"], 1)).reduceByKey(add).pprint()

def count_test(data):
	nums = data[1]
	freq = float(nums)/data.count(-1)
	return data,freq


#process.map(lambda key:(key["ip_src"], 1)).reduceByKey(add).map(lambda (x,y):(x,float(y)/testc, count)).pprint()


#process.map(lambda key:(key["ip_src"], 1)).reduceByKey(add).map(nums_count2).pprint()



#8-5day zhushi
#a.map(lambda key:(key["ip_src"], 1)).reduceByKey(add).map(nums_count2).pprint()
#print "2222222222222222222",count.value
#print type(targets.count())
s = 0
def test3(data):
	global s
	s += 1
	
	return s



def test2(data):
	#num = targ.count()
	b = data[1]/1
	return data,b	


#c = targets.map(nums_count)
#c.cache


#process.map(lambda key:key["ip_src"]).countByValue().pprint()

#b = targets.count()

#a.union(b).pprint()

#a.pprint()

#a.todf()
#a_sum = a.count()







#process.foreachRDD(sendKafka)

#process.foreachRDD(lambda rdd: rdd.foreachPartition(sendMongoDB))
#msg_stream.saveAsTextFile('out.txt')
#msg_stream.pprint()
#stream_context.checkpoint("checkpoint/")
stream_context.start()
stream_context.awaitTermination()
 
 

