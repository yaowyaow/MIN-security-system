# represent the Urls by vectors
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn import svm
import numpy as np
from urllib import quote
import string
import os
import chardet
import ast
import pickle
import pandas as pd
import json
import re
path = os.getcwd() + "/urlDetect/"
good = path + 'normal_request.txt'
bad = path + 'normal_request4.txt'
# ngram parameter
n = 2


def getdata():
    with open(good,'r') as f:
        good_query_list = [i.strip('\n') for i in f.readlines()[:]]

    with open(bad,'r') as f:
        bad_query_list = [quote(i.strip('\n'), safe=string.printable) for i in f.readlines()[:]]
    return [good_query_list, bad_query_list]

def getTransformer():
    data = getdata()
    vectorizer = TfidfVectorizer(tokenizer=get_ngrams)
    vec = vectorizer.fit(data[0])
    return vec

def getTransformer2():
    data = getdata()
    vectorizer = TfidfVectorizer(tokenizer=get_ngrams)
    vec = vectorizer.fit(data[1])
    return vec

def train():
    data = getdata()
    vec = getTransformer2()
    X_test = vec.transform(data[0]) # normal request

    X_train = vec.transform(data[1]) # bad request
    # print X_test.shape
    # print X
    # X_train, X_test= train_test_split(X, test_size=0.2, random_state=42)
    clf = svm.OneClassSVM(nu=0.001, kernel="rbf", gamma=0.1)
    clf.fit(X_train)
    y_predict_test = clf.predict(X_test)
    y_predict = clf.predict(X_train)
    n_error_test = y_predict_test[y_predict_test == -1].size
    n_error = y_predict[y_predict == -1].size
    n_error_content = np.array(data[1])[y_predict == -1]
    print n_error_test
    print n_error
    print n_error_content

    print "exporting model..."
    pickle.dump(clf, open("urlDetect3.model", 'wb'), protocol=2)
    print "exporting over"



model = pickle.load(open(path + 'urlDetect2.model', 'rb'))
# parse http packet
def parse_http_packet(data):
    start = data.find("GET")
    offset = 4
    if start == -1:
       start = data.find("POST")
       offset = 5

    end = data.find("HTTP")

    if end == -1 or start == -1:
	return '/'

    return data[start + offset: end-1]
# convert from unicode to utf-8
def recode(data):
    # return data.decode('unicode_escape').encode('utf9')
    return ast.literal_eval(data)

# load model and test once a line
def detect(data):
    data = parse_http_packet(data)
    data = [data]
    # reduce side effect of unmeaningful url
    if len(data) < 10:
        return {
            "result" : "normal"
        }
    vec = getTransformer()
    X = vec.transform(data)
    result = model.predict(X)
    if result[0] == -1:
        return {
            "result" : "abnormal"
        }
    else:
        return {
            "result": "normal"
        }

# load model and test in bulk
def detectBatch(data):
    try:
	    urls = []
	    for request in data:
		request = re.sub('"','',request)
		#request = json.loads(request) # parse string json
		urls.append(parse_http_packet(request)) # pick out the request 
	    # print(urls)
	    vec = getTransformer()
	    X = vec.transform(urls)
	    result = model.predict(X)
	    # data_dict = {
	    #     "username": [],
	    #     "uuid": [],
	    #     "request": [],
	    #     "bytes": [],
	    #     "command": [],
	    #     "src_ip": [],
	    #     "packet_type": [],
	    #     "survice": [],
	    #     "Time": [],
	    #     "dport": [],
	    #     "dst_ip": [],
	    #     "sport": [],
	    #     "data": []
	    # }
	    # df2 contains information about hostile request
	    # df2 = pd.DataFrame(data_dict)
	    res = []
	    res_in_tuples = []
	    urlCounter = 0  # counter for traversal in reverse, if you want to resume, set it to 0 
	    last_head_packet = 'a'
	    # abnormalCounter = 0 # counting the number of abnormal requests
	    model2 = pickle.load(open(path + 'urlDetect3.model', 'rb'))
	    for ans in result: # abnormal request [-1 1], reversed result means we will generate res in tuples 
		if eval(data[urlCounter])['data'][0:6] == '\u0005' or eval(data[urlCounter])['data'][0:6] == '\u0006': # to generate tuples in sequent way
		    last_head_packet = urlCounter
		    print('last_head_packet')
		# print(eval(data[urlCounter])['data'][0])
		if ans == -1: # generate the information of abnormal request
		    sus_url = parse_http_packet(data[urlCounter])
		    temp = sus_url
		    # temp = filter(str.isalpha, sus_url)
		    # print temp
		    # df2.loc[abnormalCounter] = data.iloc[urlCounter]
		    if len(temp) > 10: # eliminate the effect of invalid request
			t_result = model2.predict(getTransformer2().transform([sus_url]))
			# print t_result
			if t_result[0] == 1:
			    res.append(data[urlCounter])
			    res_in_tuples.append((last_head_packet, urlCounter))
                            # print(res_in_tuples)
			    #if last_mag_packet != '':
				#res_in_tuples.append((data[urlCounter + 1], last_mag_packet))
			    
			elif len(temp) > 30:
			    res.append(data[urlCounter])
			    res_in_tuples.append((last_head_packet, urlCounter))
			    # print(res_in_tuples)

			    #if last_mag_packet != '':
				#res_in_tuples.append((data[urlCounter + 1], last_mag_packet))
		    	 	#print("last_mag_packet_update3")
			    #last_mag_packet = data[urlCounter]
		    else:
			result[urlCounter] = 1
		urlCounter += 1
            # print(res_in_tuples)
	    return res_in_tuples
    except:
	print("error")
	return []


# tokenizer function, this will make 3 grams of each query
def get_ngrams(query):
    tempQuery = str(query)
    ngrams = []
    for i in range(0, len(tempQuery)-n):
        ngrams.append(tempQuery[i:i+n])


    return ngrams

#data = "{'username': 'null', 'uuid': 'null', 'request': '/min/gdcni10', 'bytes': 1249, 'command': 'null', 'src_ip': '58.60.1.47', 'packet_type': 'data_packt', 'survice': 0, 'Time': '2020-10-12 08:58:28', 'dport': 6363, 'dst_ip': '121.15.171.90', 'sport': 2172, 'data': u'd\xfd\x04\xb5P\xfd\x04"\xb1\x05\xfd\x04\xad\x07\xfd\x01O\x08\x03min\x08\x07gdcni10\x08\tvpnserver\x08\x0219\x08\x045724\x08\x16 \x1b\x01\x01\x1c\x1b\x07\x19\x08\x08d2doNQ--\x08\x03KEY\x08\x08\xa5Xf \x07\xf7\xcd_\x08\xfd\x01\x04\x17\xfd\x01\x00F\x03\x9d\'\x19\x04\x9dM\xeb@^\x08-<1^\x1c\xfe\x16\xac\x8c\x98\x1c\xf8\xb0\xba\\\xc6\xe8\xb7D\x03\x1f\x85\xe8\xee\xc1[\x1e\x96\x94G\x18#\x99\xa0K\xf8\'\xa4 E\xbb\xad\x94t0\xf0\xffm\x9eg\x0c\xb2\x88U\xff]\x934\xe8$\x0c\xb2\xfcT\x02\x1a\xcb\xe1\xb3WS=\xb9@%:C\x1aF\x8d\xd1\xc4u\xd2\x83\x82\x8e\x06\xc9\xaf\xb6(\x9f\xcd\xdfn!\x83\x85]X\x04\xb71\xef\x04\xafC\xf0\x80\x0fb\xbd\xd6\xb5\xfahV2\xf9\xea\xc1\x89\xdeo\xdb\x17rk\xd2\xf4\x14K\x11\xca\xc1\xe0*\x91\xc0V\x84\xf0\x914\xe6v\xf7\xde\xc8kY\xf88D\x8e\xf67\x93Rx\xbfTDm\x95)\xcd\xfc\xa9M\xfel\xa5\x15d\xad\xfe:\x8c\x14\xe6\xa1`[\x13kF\xf3\xc2\x93\xfa<Eb9s\x16\x9fI^AH:T\x88\xfb\x96\xb6/\xaf!\xe4\xfc\xdf?\xd3\xa7\xd4\xce\xcf\xf2^\x95\x143\x11\xfa\x80\xf8spq\xef|\x8co~F\x98\xf2\xc7\xa6\xaf!\x00\x12\x00\n\x04}\xbb\x16\xef$\xfd\x03L\x01\x00\x00\x16\\\x05\x00\x00\x03B\x00\x00\x03>\x02\x00\x00\x00\nGET /vulnerabilities/sqli/?id=1%27or%271%27%3D%271&Submit=Submit&user_token=1850b4bebc78396980d2b4c5063011ba HTTP/1.1\r\nHost: 172.16.254.2:8080\r\nConnection: keep-alive\r\nUpgrade-Insecure-Requests: 1\r\nUser-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.75 Safari/537.36\r\nAccept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9\r\nReferer: http://172.16.254.2:8080/vulnerabilities/sqli/?id=1%27or%271%27%3D%271&Submit=Submit&user_token=66803174bd9fd8c09ffb9d0ea62180a1\r\nAccept-Encoding: gzip, deflate\r\nAccept-Language: zh-CN,zh;q=0.9\r\nCooki"
