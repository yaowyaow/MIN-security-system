# -*- coding:utf-8 -*-
 
from socket import *
import json
import struct

HOST = '121.15.171.91' # or 'localhost'
PORT = 8010
BUFSIZ =1024
ADDR = (HOST,PORT)

def block_message(data):
	tcpCliSock = socket(AF_INET,SOCK_STREAM)
	tcpCliSock.connect(ADDR)
	data = {"Type":"network", "Command":"Log", "Prefix":"/mis/update/danger_log", "Level":1, "Action":"test", "Sig":"xxx", "Timestamp":"xxx"}
	json_data = json.dumps(data)
	#data = str(data)
	#head_bytes=bytes(json.dumps(json_data))
	head_bytes = bytes(json.dumps(data))
	head_len_bytes=struct.pack('<i',len(head_bytes))
	tcpCliSock.send(head_len_bytes)
	#tcpCliSock.send(head_bytes)
	tcpCliSock.sendall(head_bytes)
	data1 = tcpCliSock.recv(BUFSIZ)
	print(data1)
	#.decode('utf-8'))
	tcpCliSock.close()
