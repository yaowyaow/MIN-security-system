#!/usr/bin/python
# encoding: utf-8
# -*- coding: utf8 -*-


import os
import sys
import time
import argparse


import logging

def getcwd():
	return os.getcwd()

class Logger:
    def __init__(self,loggername):

        #创建一个logger
        self.logger = logging.getLogger(loggername)
        self.logger.setLevel(logging.DEBUG)

	log_path = getcwd()

        #创建一个handler，用于写入日志文件
	log_path = log_path + "/logs/"
	if not os.path.exists(log_path):
		os.makedirs(log_path)
        logname = log_path + 'out.log' #指定输出的日志文件名
        fh = logging.FileHandler(logname,encoding = 'utf-8')  # 指定utf-8格式编码，避免输出的日志文本乱码
        fh.setLevel(logging.DEBUG)

        #创建一个handler，用于将日志输出到控制台
        #ch = logging.StreamHandler()
        #ch.setLevel(logging.ERROR)

        # 定义handler的输出格式
        #formatter = logging.Formatter('%(asctime)s-%(name)s-%(levelname)s-%(message)s')
	formatter = logging.Formatter('[%(levelname)s] - %(asctime)s - process: %(process)d  - %(name)s - %(module)s ->\n %(message)s\n')
        fh.setFormatter(formatter)
        #ch.setFormatter(formatter)

        # 给logger添加handler
        self.logger.addHandler(fh)
        #self.logger.addHandler(ch)

    def get_log(self):
        """孾Z举I䷾@个佇½录°﻾L佛~^课Clogger孾^佾K"""
        return self.logger

	
class event_Logger():
    def __init__(self,loggername):
	#set another log which only display the attack event
	self.event_logger = logging.getLogger(loggername)
        self.event_logger.setLevel(logging.DEBUG)
	self.event_logger.propagate = False

	log_path = getcwd()
        log_path = log_path + "/logs/"
        if not os.path.exists(log_path):
                os.makedirs(log_path)
        logname = log_path + 'event.log' 
        fh2 = logging.FileHandler(logname,encoding = 'utf-8')  
        fh2.setLevel(logging.DEBUG)

        ch2 = logging.StreamHandler()
        ch2.setLevel(logging.DEBUG)

        formatter = logging.Formatter('[%(levelname)s] - %(asctime)s - process: %(process)d  - %(name)s - %(module)s ->\n %(message)s')
        fh2.setFormatter(formatter)
        ch2.setFormatter(formatter)

        # 纾Ylogger添佊| handler
        self.event_logger.addHandler(fh2)
        #self.event_logger.addHandler(ch2)
	
    def get_event_log(self):
	return self.event_logger


if __name__ == '__main__':
    t = Logger("hmk").get_log().critical("User %s is loging" )
    #Logger("update").get_log().warning("test")
    a = {'a':1}
    event_Logger("even23423423t_log").get_event_log().debug(a)
