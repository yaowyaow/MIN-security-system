#coding=utf-8
import threading
import os
import spark_analyze
import net_message
import S_Assessment

def exec_spark_ip():
    try:
	#os.system("python spark_analyze.py 'all'")
	os.system("python spark_analyze.py 'ip'")
    except Exception as e:
	print e
	exit()

def exec_spark_min():
    try:
        #os.system("python spark_analyze.py 'all'")
        os.system("python spark_analyze.py 'min'")
    except Exception as e:
        print e
        exit()


def exec_net():
    try:
	os.system("python net_message.py -dv")
    except Exception as e:
	print e
	exit()

def exec_sa():#态势评估
    try:
	#os.system("python S_Assessment.py")
	test = S_Assessment.S_Assessment()
	test.run(1)
    except Exception as e:
	print e
	exit()

if __name__ == "__main__":
	t_1 = threading.Thread(target=exec_spark_ip)
	t_2 = threading.Thread(target=exec_spark_min)
	t_2.setDaemon(True)
	t_3 = threading.Thread(target=exec_sa)
	t_3.setDaemon(True)
	t_4 = threading.Thread(target=exec_net)
        t_4.setDaemon(True)
	t_1.start()
	t_2.start()
	t_3.start()
	t_4.start()
