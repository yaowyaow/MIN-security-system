# represent the Urls by vectors

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn import svm
import numpy as np
from urllib import quote
import string
import os
import pickle
import pandas as pd
import json
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
# load model and test once a line
def detect(data):
    data = [data]
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
    urls = []
    for request in data:
	request = eval(request)
        #request = json.loads(request) # parse string json
        urls.append(request['request']) # pick out the request 
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
    urlCounter = 0  # counter for traversal
    # abnormalCounter = 0 # counting the number of abnormal requests
    model2 = pickle.load(open(path + 'urlDetect3.model', 'rb'))
    for ans in result: # abnormal request [-1 1]
        if ans == -1: # generate the information of abnormal request
            temp = filter(str.isalpha, eval(data[urlCounter])['request'])
            print temp
            # df2.loc[abnormalCounter] = data.iloc[urlCounter]
            if len(temp) > 10: # eliminate the effect of invalid request
                t_result = model2.predict(getTransformer2().transform([eval(data[urlCounter])['request']]))
                print t_result
                if t_result[0] == 1:
                    res.append(data[urlCounter])
                elif len(temp) > 30:
                    res.append(data[urlCounter])
            else:
                result[urlCounter] = 1
        urlCounter += 1
    return res


# tokenizer function, this will make 3 grams of each query
def get_ngrams(query):
    tempQuery = str(query)
    ngrams = []
    for i in range(0, len(tempQuery)-n):
        ngrams.append(tempQuery[i:i+n])


    return ngrams

