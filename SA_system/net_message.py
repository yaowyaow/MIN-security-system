#!/usr/bin/python
# encoding: utf-8
# -*- coding: utf8 -*-


import os
import sys
import threading
from scapy.all import *
from mongodb import *
import time
import re
import argparse
from utils import *
import userFrequency
from IPy import IP as IPTEST
#import Queue
try:
    import netifaces
except ImportError:
    try:
        command_to_execute = "pip install netifaces || easy_install netifaces"
        os.system(command_to_execute)
    except OSError:
        print "Can NOT install netifaces, Aborted!"
        sys.exit(1)
    import netifaces
try:
    from scapy.all import *
except ImportError:
    try:
        command_to_execute = "pip install scapy || apt-get install python-scapy"
        os.system(command_to_execute)
    except OSError:
        print "Can NOT install scapy, Aborted!"
        sys.exit(1)
    import netifaces

class captureModule(object):

	def __init__(self):
		self.logger = Logger(__name__).get_log()
		self.logger.propagate = False
		#self.logger.info("test")
		#self.event_logger = event_Logger(__name__).get_event_log()

	def getSysMessage(self):
		routingGateway = netifaces.gateways()['default'][netifaces.AF_INET][0]
		routingNicName = netifaces.gateways()['default'][netifaces.AF_INET][1]
 
		for interface in netifaces.interfaces():
				if interface == routingNicName:
					# print netifaces.ifaddresses(interface)
						routingNicMacAddr = netifaces.ifaddresses(interface)[netifaces.AF_LINK][0]['addr']
						try:
							routingIPAddr = netifaces.ifaddresses(interface)[netifaces.AF_INET][0]['addr']
								# windows don' support netifaces
							routingIPNetmask = netifaces.ifaddresses(interface)[netifaces.AF_INET][0]['netmask']
						except KeyError:
								pass
	
		display_format = '%-30s %-20s'
		print display_format % ("Routing Gateway:", routingGateway)
		print display_format % ("Routing NIC Name:", routingNicName)
		print display_format % ("Routing NIC MAC Address:", routingNicMacAddr)
		print display_format % ("Routing IP Address:", routingIPAddr)
		print display_format % ("Routing IP Netmask:", routingIPNetmask)
		return {"routingGateway":routingGateway, "routingNicName":routingNicName, "routingNicMacAddr":routingNicMacAddr, "routingIPAddr":routingIPAddr, "routingIPNetmask":routingIPNetmask}

	ttlValues = {}
	THRESH = 5
	def build_packet_callback1(self, log_queue):
		def checkTTL(ipsrc, ttl):
			    if IPTEST(ipsrc).iptype() == 'PRIVATE':
				return
			    if not ttlValues.has_key(ipsrc):
				pkt2 = sr1(IP(dst=ipsrc) / ICMP(), retry=0, timeout=1, verbose=0)
				ttlValues[ipsrc] = pkt2.ttl
			    if abs(int(ttl) - int(ttlValues[ipsrc])) > THRESH:
				print('\n[!] Detected Possible Spoofed Packet From: ' + ipsrc)
				print('[!] TTL: ' + ttl + ', Actual TTL: ' + str(ttlValues[ipsrc]))

		def packet_callback(pkt):
			#self.logger.info("test***!!!")
			if args.view:
				print "\n***************packet***************"
			data_dict = {}
			if Raw in pkt:
				try:
					data_dict["src_ip"] = pkt[IP].src	
					data_dict["dst_ip"] = pkt[IP].dst
					data_dict["sport"] = pkt.sport
					data_dict["dport"] = pkt.dport
					data_dict["bytes"] = pkt.len
					data_dict["data"] = pkt[Raw].load
					data_dict['Time'] = time.strftime('%Y-%m-%d %H:%M:%S')
					log_queue.put(data_dict)
				except:
					print "extracet fail"

			'''if pkt.dport != 22:
				if args.view:
					print "\n*********every pkg analyze:*******"
					#print pkt
				data_dict = {}
				if args.scan_detect:
					#checkTTL(pkt[IP].src, pkt.ttl)
					pass

				if Raw in pkt:
					#提取端口地址信息
					try:
						data_dict["src_ip"] = pkt[IP].src
						data_dict["sport"] = pkt.sport
						data_dict["dport"] = pkt.dport
						
						#解析，提取包内关键信息
						NDN_packet = pkt[Raw].load
						#print "packet++++:" + NDN_packet
						if NDN_packet[0] == '\x05': #兴趣包标志位
							data_dict["packet_type"] = "interest_packet"
						elif NDN_packet[0] == '\x06': #数据包标志位
							data_dict["packet_type"] = "data_packet"
						else:
							data_dict["packet_type"] = "data_packt"
							
						if args.view:
							print "port ip success"
				

						#正则表达式提取前缀请求 repr防止packet转义,re.I忽视大小写
						request_re = re.search(r'(\\x08\\x([0-9,a-f]){2}([0-9,a-z])*)+',repr(NDN_packet), re.I).group()
						request = re.sub(r'\\x08\\x([0-9,a-f]){2}', '/', request_re)
						data_dict["request"] = request
						if args.view:
							print "request success"
						#提取请求信息
						#message = re.search(r'\{[^\\]*\}',repr(NDN_packet), re.I).group()
						#message = re.search(r'\{((\n)*?([\:\w\"\s\,])*?)*?(\".*?\")*?\}',repr(NDN_packet), re.I).group()
						#非贪婪模式json
						#message = re.search(r'\{((\".*?\")\:(\".*?\")(\,)*?)*?\}', repr(NDN_packet), re.I).group()
						#将非法字符（空格回车）替换
						message = re.sub(r'[(\n)|\s]*','',NDN_packet)
						message = re.search(r'\{((\n)*?([\:\w\"\s\,])*?)*?(\".*?\")*?\}',(message), re.I).group()

						message_dict = eval(message)
						#data_dict["message"] = message_dict
						data_dict["message"] = repr(NDN_packet)
						if args.view:
							print "message success"
						#提取身份信息和访问接口信息
						if 'username' in message:
							data_dict["username"] = message_dict["username"]
						else:
							data_dict["username"] = None
							raise    #跳入except	
						if 'command' in message:
							data_dict["command"] = message_dict["command"]
						else:
							data_dict["command"] = None
							raise
						if 'uuid' in message:
							data_dict["uuid"] = message_dict["uuid"] 
						else:
							data_dict["uuid"] = None
						if args.view:
							print "username success"
						#插入时间信息
						data_dict['Time'] = time.strftime('%Y-%m-%d %H:%M:%S')
						self.logger.info(data_dict)
						log_queue.put(data_dict)
						
						if args.view:
							print "\n=========数据包提取=======\n" + str(data_dict) +"\n"
					except:
						#代表信息提取失败，packet不符合预置格式
						if args.view:
							print "message don't match the pattern"
						if args.detail:
							print "\n============非NDN格式数据包============\n" 
							try:
								self.logger.error(repr(NDN_packet))
								print repr(NDN_packet)
							except:
								pass

						if args.port == -1:
							#print "shibai+++++++++++++++++",data_dict
							log_queue.put(data_dict)
							#print "*****************",log_queue.get()
						pass
				else:
					if args.detail:
						self.logger.error(repr(pkt))
						print repr(pkt)
						#print pkt.dport

				
		'''	
		return packet_callback
	
	def analyze(self):
		return 1

	def run(self, log_queue):
		#NicName = str(self.getSysMessage()["routingNicName"])
		#time.sleep(0.5)
		print 'start capture:'
		if args.port == -1:
			filter_set = "tcp or udp"
		else:
			filter_set = "port " + str(args.port)

		if args.interface:
			if args.interface == "any":
				dpkt = sniff(store=args.save_packet,prn=self.build_packet_callback1(log_queue), filter=filter_set)
			else:
				NicName = args.interface
				dpkt = sniff(store=args.save_packet,iface=NicName,prn=self.build_packet_callback1(log_queue), filter=filter_set)
		else:
			NicName = str(self.getSysMessage()["routingNicName"])
			dpkt = sniff(store=args.save_packet, iface=NicName,prn=self.build_packet_callback1(log_queue), filter=filter_set)

		if args.save_packet:
			wrpcap("packet.pcap", dpkt)
			'''#解析数据包为可读
			print '所抓的包已经保存'

			pcks = rdpcap('demo.pcap')
			print '开始解析pcap包'

			# 输出重定向  讲在控制台的输出重定向到 txt文本文件中
			output = sys.stdout
			outputfile = open('capture.txt', 'w')
			sys.stdout = outputfile

			zArp = 0
			zIcmp = 0
			ipNum = set()

			for p in pcks:
				status1 = p.payload.name  # 可能是ARP的报文
				status2 = p.payload.payload.name  # 可能是TCP报文 也可能是ICMP的报文

			# p.show() 输出报文， 在符合的情况下
			if status1 == 'IP':
				ipNum.add(p.payload.src)  # 将ip报文的源地址，和目的地址存在set集合>里面（set去重）
				ipNum.add(p.payload.dst)
				p.show()
				print ''
			else:
				if status1 == 'ARP':
					p.show()
				print ''
				zArp += 1

				if status2 == 'ICMP':
					p.show()
				print ''
				zIcmp += 1
			print 'IP：' + str(len(ipNum)) + ' ARP：' + str(zArp) + ' ICMP：' + str(zIcmp) # 报文数量的输出

			outputfile.close()
			sys.stdout = output  # 恢复到控制台输出

			print '输出结束'
			print dpkt
			'''
	


if __name__ == "__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument('-p','--port', default=6363,help="port, -1 means to listen all ports", type=int)
	parser.add_argument('-i', '--interface', default='', help = "choose interface to capture data, 'any' means all interface", type=str)
	parser.add_argument('-s', '--strong', action='store_true', help="strong mode, analyze every packet, deny the dangerous data.")
	parser.add_argument('-v', '--view', action='store_true',help="open the view mode, view the packet message")
	parser.add_argument('-t', '--time', action='store_true', help="add the time to every packet in the controller")
	parser.add_argument('-d', '--detail', action='store_true', help="view the detailed packet message")
	parser.add_argument('-sp', '--save_packet', action='store_true', help="save the packet message to pcap file")
	parser.add_argument('-sn', '--scan_detect', action='store_true', help="save the packet message to pcap file")


	args = parser.parse_args()

	#消息队列，防止线程之间数据交换冲突
	import Queue
	log_queue = Queue.Queue()
	#workerThread = []

	cpt = captureModule()
	mgodb = mongoOperate("packet_flow", "packet_flow")
	#抓获数据包，入队列
	t_cpt = threading.Thread(name="capture", target=cpt.run, args=(log_queue,))
	#t_cpt.setDaemon(True)
	t_cpt.start()
	#cpt.run(log_queue)
	#从队列中获取数据，插入数据库
	t_mgodb = threading.Thread(name="mongo_operate", target=mgodb.run, args=(log_queue,args.strong,))
	t_mgodb.setDaemon(True)
	t_mgodb.start()
	#captureModule().capture()
	#t_mgodb2 = threading.Thread(name="mongo_operate", target=mgodb.run, args=(log_queue,args.strong,))
        #t_mgodb2.setDaemon(True)
        #t_mgodb2.start()

	t_userFreq = threading.Thread(name="user frequency", target=userFrequency.run(), args=())
	t_userFreq.setDaemon(True)
	t_userFreq.start()

