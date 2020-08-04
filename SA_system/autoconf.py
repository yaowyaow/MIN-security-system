#coding=utf-8
#修改时搜索目录即可
import os
import sys
import argparse
import time
import threading

def pmacctd_start():
	cmd_check = "ps -aux | grep pmacct | wc -l"
	nums = os.system(cmd_check)
	if nums > 2:
		print "pmacctd has already been running"
		pmacctd_shutdown()
	cmd_start = " pmacctd -f /home/gdcni19/xin777/librdkafka/pmacct/pmacctd2.conf >/dev/null"
	try:
		os.system(cmd_start)
		print "pmacctd started"
	except Exception as e:
		print e

def pmacctd_shutdown():
        file_ = os.popen("ps -aux | grep pmacct")
        text = file_.read()
        file_.close()

        pid_list = []
        for each in text.split("\n"):
                if ("grep" not in each) and each:
                        pid_list.append(each.split()[1])
        print pid_list

        #kill the pids
        for pid in pid_list:
                cmd = "kill -s 9 " + pid
                try:
                        os.system(cmd)
                        print pid + " killed"
                except:
                        print "kill failed"


def kafka_start_zookeeper():
	cmd_check_zookeeper = "ps -aux | grep zookeeper.properties | wc -l"
	nums = os.system(cmd_check_zookeeper)
	if nums > 2:
		print "zookeeper.properties has been running"
		kafka_shutdown()
	
	cmd_start_zookeeper = "/home/gdcni19/xin777/kafka_2.13-2.5.0/bin/zookeeper-server-start.sh /home/gdcni19/xin777/kafka_2.13-2.5.0/config/zookeeper.properties >/dev/null"
	try:
		print "kafka zookeeper started"
                os.system(cmd_start_zookeeper)
        except Exception as e:
                print e


def kafka_start_server():
	cmd_check_server = "ps -aux | grep server.properties | wc -l"
        nums2 = os.system(cmd_check_server)
        if nums2 > 2:
                print "server.properties has been running"
		kafka_shutdown()
                #kafka_shutdown()

	cmd_start_server = "/home/gdcni19/xin777/kafka_2.13-2.5.0/bin/kafka-server-start.sh /home/gdcni19/xin777/kafka_2.13-2.5.0/config/server.properties >/dev/null"
	try:
		print "kafka server started"
		os.system(cmd_start_server)
	except Exception as e:
		print "kafka_server failed\n " , e
	print "kafka started"


def kafka_shutdown():
	file_ = os.popen("ps -aux | grep zookeeper.properties")
        text = file_.read()
        file_.close()

        pid_list = []
        for each in text.split("\n"):
                if ("grep" not in each) and each:
                        pid_list.append(each.split()[1])
        print pid_list

        #kill the pids
        for pid in pid_list:
                cmd = "kill -s 9 " + pid
                try:
                        os.system(cmd)
                        print pid + " killed (zookeeper)"
                except:
                        print "kill zookeeper failed"

	file_ = os.popen("ps -aux | grep server.properties")
        text = file_.read()
        file_.close()

        pid_list = []
        for each in text.split("\n"):
                if ("grep" not in each) and each:
                        pid_list.append(each.split()[1])
        print pid_list

        #kill the pids
        for pid in pid_list:
                cmd = "kill -s 9 " + pid
                try:
                        os.system(cmd)
                        print pid + " killed(server.properties)"
                except:
                        print "kill server.properties failed"


def hadoop_start():
        cmd_start = "su hadoop -c /usr/local/hadoop/sbin/start-dfs.sh >/dev/null"
        try:
                os.system(cmd_start)
                print "hadoop started"
        except Exception as e:
                print e

def hadoop_shutdown():
	cmd_stop = "su hadoop -c /usr/local/hadoop/sbin/stop-dfs.sh"
	try:
		os.system(cmd_stop)
		print "hadoop stopping"
	except Exception as e:
		print e


def all_shutdown():
	t_kafka = threading.Thread(name="kafka",target=kafka_shutdown, args=())
	t_pmacctd = threading.Thread(name="pmacct", target=pmacctd_shutdown, args=())
	t_hadoop = threading.Thread(name="hadoop", target=hadoop_shutdown, args=())
	t_kafka.start()
	t_pmacctd.start()
	t_hadoop.start()

def test_kafka():
	import json
	from kafka import KafkaProducer

	try:
		producer = KafkaProducer(bootstrap_servers='localhost:9092')

		producer.send('test_rhj', "test")
		print "kafka is running"
		producer.close()
	except Exception as e:
		print "\n\n\n***********************************\nkafka server start failed "
		print "ERROR: ",e
		print "=======================================\nplease run the command : \nsudo /home/gdcni19/xin777/kafka_2.13-2.5.0/bin/kafka-server-start.sh /home/gdcni19/xin777/kafka_2.13-2.5.0/config/server.properties\n====================================\n\n\n"



if __name__  == "__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument('-r', '--restart', action="store_true", help="restart the pmacct, kafka, hadoop")
	parser.add_argument("-s", "--shutdown", action = "store_true", help="shutdown the kafka, pmacct, hadoop")
	parser.add_argument("-t", "--test", action = "store_true", help="test the kafka is running")
	args = parser.parse_args()
	if len(sys.argv) < 2:
		print "usage: -h to learn more"
		print "please run the -s first"

		

	elif args.restart:
		all_shutdown()
		t_kafka_zookeeper = threading.Thread(name="kafka_zookeeper",target=kafka_start_zookeeper, args=())
		t_kafka_server = threading.Thread(name="kafka_server",target=kafka_start_server,args=())
		t_pmacctd = threading.Thread(name="pmacct", target=pmacctd_start, args=())
		t_hadoop = threading.Thread(name="hadoop", target=hadoop_start, args=())
		#t_kafka_zookeeper.setDaemon(True)
		t_kafka_zookeeper.start()

		t_kafka_server.start()

		time.sleep(3)
		test_kafka()

		time.sleep(7)
		#t_pmacctd.setDaemon(True)
		#t_hadoop.setDaemon(True)
		t_pmacctd.start()
		t_hadoop.start()

	elif args.shutdown:
		t_kafka = threading.Thread(name="kafka",target=kafka_shutdown, args=())
                t_pmacctd = threading.Thread(name="pmacct", target=pmacctd_shutdown, args=())
                t_hadoop = threading.Thread(name="hadoop", target=hadoop_shutdown, args=())
                t_kafka.start()
                t_pmacctd.start()
                t_hadoop.start()
	
	elif args.test:
		test_kafka()
