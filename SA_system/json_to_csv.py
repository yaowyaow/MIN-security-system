# coding=utf-8

import json
import csv 
from kafka import KafkaConsumer
# 重新进行配置读写数据时的默认编码
import sys
reload(sys)
sys.setdefaultencoding('utf-8')


def json_to_csv():

    # 1.读取json文件的数据
    #json_file = open('my.json', 'r')
    json_list = []
    for line in open('test_data.json', 'r'):
	json_list.append(json.loads(line))
    # 2. csv的写入文件对象
    csv_file = open('test_data.csv', 'w')
    # 3. 取出数据 : 1.表头 2. 内容
    #json_list = json.load(json_file)
    # 3.1获取表头所需要的数据
    sheet_title = json_list[0].keys()
    # 3.2 取所有内容
    json_values = []
    for dict in json_list:
        json_values.append(dict.values())


    # 4.写入csv文件
    # 4.1根据文件对象  生成读写器
    csv_writer = csv.writer(csv_file)

    # 4.2 写入表头
    csv_writer.writerow(sheet_title)
    # 4.3 写入内容
    csv_writer.writerows(json_values)

    # 5.关闭文件
    csv_file.close()
    #json_file.close()

    print("存完了")

if __name__ == '__main__':
    json_to_csv()
'''
    consumer = KafkaConsumer('test',bootstrap_servers=['127.0.0.1:9092'])
    count = 0
    answer = 0
    json_values = []
    csv_file = open('test-topic-data.csv', 'w')
    for message in consumer:
	count += 1
	data = eval(message.value)
	if data["ip_src"] == "121.15.171.84":
		answer += 1
	if count == 1:
		sheet_title = data.keys()
	if count < 40000:
		json_values.append(data.values())
		print count
	elif count == 40000:
		csv_writer = csv.writer(csv_file)
		csv_writer.writerow(sheet_title)
		csv_writer.writerows(json_values)
		csv_file.close()
		print "save success"
		print "answer: ", answer
	else: 
		break
'''
