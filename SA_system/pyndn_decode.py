import ctypes
import sys
from socket import *
import pytest
import struct
from ndn.encoding import Name, Component
import ndn

def test_decode_func(data):
	#print(len(data))
	data = bytearray(data.encode('raw_unicode_escape'))#unicode to bytes utf-8
	if data[0] == 6:
		try:
			decode_data = ndn.encoding.ndn_format_0_3.parse_data((data), with_tl = True)[3]   #data_packet
			print(decode_data.signature_info, '\n', decode_data.signature_info.key_locator)
			#print(decode_data)
			return decode_data.signature_info.key_locator
		except Exception as e:
			print('data packet parse error:', str(e))
			return 'data packet parse error:'+str(e)
	elif data[0] == 5:
		try:
			decode_data = ndn.encoding.ndn_format_0_3.parse_interest((data), with_tl = True)
			#print(decode_data)
			print(decode_data, '\n', bytes(decode_data[0][-2]))
			return bytes(decode_data[0][-2])
		except Exception as e:
			print('interest packet parse error:',str(e))
			return 'interest packet parse error:'+str(e)
	else:
		print("not match pattern\n", data[0],'\n',data)
		return 'not match pattern'

if __name__ == "__main__":

	#string = (sys.argv[1]).encode('utf-8').decode('unicode_escape')#make \ not translate to \\
	#string = st.encode('utf-8').decode('unicode_escape')
	#print(string,'\n',type(string1))
	with open('evil_data.txt', 'r') as f:
		string = f.read()
	string = string.encode('utf-8').decode('unicode_escape')
	test_decode_func(string)
