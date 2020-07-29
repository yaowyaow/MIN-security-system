import os
import sys

#get thread pid
file_ = os.popen("ps -aux | grep net_message.py")
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

