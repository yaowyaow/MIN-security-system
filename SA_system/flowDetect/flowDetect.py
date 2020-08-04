#coding=utf-8
from sklearn import preprocessing
from sklearn.preprocessing import LabelEncoder
import pandas
import pickle
import json
import os
from utils import *
path = os.getcwd() + "/" 
print path
nmapModel = pickle.load(open(path+'flowDetect/ddosmodel.model', 'rb'))
model = pickle.load(open(path+'flowDetect/ddosmodel.model', 'rb'))
def ddos_detect(data):
    headers=["Transport Layer", "Source IP","Dest IP","Source Port","Dest Port","Attack Length"]
    data_dict = {}
    for header in headers:
        data_dict[header] = []
        
    for i in range(len(data)):
        temp = json.loads(data[i])
        data_dict["Transport Layer"].append(temp["Transport Layer"])
        data_dict["Source IP"].append(temp["Source IP"])
        data_dict["Dest IP"].append(temp["Dest IP"])
        data_dict["Source Port"].append(temp["Source Port"])
        data_dict["Dest Port"].append(temp["Dest Port"])
        data_dict["Attack Length"].append(temp["Attack Length"])

    # print data_dict
    df = pandas.DataFrame(data_dict)
    print df["Source IP"].value_counts()
    
    row_num = df.shape[0]
    if row_num > 5000:
        if (df["Source IP"].value_counts()[0] * 1.0 / (row_num * 1.0 )) > 0.5:
            ip = df["Source IP"].value_counts().index[0]
            df.loc[df["Source IP"] == ip, ["Attack Length"]] = 1

    # data = LiveLabelEncoding("ddosDataAdjusted4.csv", df)
    X = df[['Transport Layer', 'Source IP', 'Dest IP', 'Source Port', 'Dest Port',
            'Attack Length']]
    X = LiveLabelEncoding(path+"flowDetect/ddosDataAdjusted4.csv", X)

    scaler = preprocessing.StandardScaler().fit(X)

    # X = scaler.transform(data)[-1, :].reshape(1, -1)
    X = scaler.transform(X)[-row_num:, :]
    # y = df["Target"]
    # realHostile = y.sum()
    prediction = model.predict(X)
    # print(prediction)
    hostile = 0  # this block counts how many 'hostile' packets have been predicted by the model
    safe = 0
    data_dict = {
        "Transport Layer": [],
        "Source IP": [],
        "Dest IP": [],
        "Source Port": [],
        "Dest Port": [],
        "Attack Length": []
    }
    # df2 contains information about hostile flow
    df2 = pandas.DataFrame(data_dict)
    num1 = 0 # counter of df2
    ddos_counter = 0
    for check in prediction:
        if check == 1:  # change to 0 to force ddos attack
            if num1 == 0:
                df2.loc[num1] =  df.iloc[ddos_counter]
                num1 += 1
            hostile += 1
        else:
            safe += 1
        ddos_counter += 1
    # if prediction == 0:
    #     predicted_class = 'normal'
    # elif prediction == 1:
    #     predicted_class = 'ddos attack'
    print("DDos Safe Packets: ", safe)
    print("DDos Hostile Packets Detected: ", hostile)
    print("DDos Suspicious Packets Info: \n")
    print(df2)
    # print("Actually Hostile Packets Detected: ", corr)
    # print("Actually Hostile Packets: ", realHostile)
    #write to the log file

    return {
        # 'Prediction': predicted_class
        'Safe Packets Detected': str(safe),
        'Hostile_Packets_Detected': str(hostile),
        "Hostile_Packets_Info": df2.to_json(orient="records") # convert dataframe to json
    }

def nmap_detect(data):
    headers=["Transport Layer", "Source IP","Dest IP","Source Port","Dest Port","Attack Length"]
    data_dict = {}
    for header in headers:
        data_dict[header] = []
        
    for i in range(len(data)):
        temp = json.loads(data[i])
        data_dict["Transport Layer"].append(temp["Transport Layer"])
        data_dict["Source IP"].append(temp["Source IP"])
        data_dict["Dest IP"].append(temp["Dest IP"])
        data_dict["Source Port"].append(temp["Source Port"])
        data_dict["Dest Port"].append(temp["Dest Port"])
        data_dict["Attack Length"].append(temp["Attack Length"])

    df = pandas.DataFrame(data_dict)
    # print(df.loc[:, ['Source IP', 'Dest IP']])
    row_num = df.shape[0]
    X = df[['Transport Layer', 'Source IP', 'Dest IP', 'Source Port', 'Dest Port',
            'Attack Length']]
    port_data = {} # record all port access data
    frequency_data = {}
    if True:    
	for index, row in X.iterrows():
        # print row
	    access = ((row['Source IP'], row['Dest IP']), row['Dest Port'])
        # print access
            if access[0] not in port_data:
                port_data[access[0]] = []
                port_data[access[0]].append(access[1])
                frequency_data[access[0]] = 1
            elif access[1] not in port_data[access[0]]:
                port_data[access[0]].append(access[1])
                frequency_data[access[0]] += 1
    
    max_port_num = -1
    max_key = ''
    port_num_sum = 0
    for key in frequency_data:
        if frequency_data[key] > max_port_num:
            max_port_num = frequency_data[key]
            max_key = key
        port_num_sum += frequency_data[key]
    print frequency_data[max_key]
    print max_key
    
    X.loc[:,['Attack Length']] = 0
    if max_key != '':
        if row_num < 3500 and frequency_data[max_key] >= 10 and max_key[0] != '121.15.171.82':
            X.loc[(X['Source IP'] == max_key[0]) & (X['Dest IP'] == max_key[1]), ['Attack Length']] = 1
    
    # print X
    
    X = LiveLabelEncoding(path+"flowDetect/ddosDataAdjusted4.csv", X)
    scaler = preprocessing.StandardScaler().fit(X)
    X = scaler.transform(X)[-row_num:, :]
    data_dict = {
        "Transport Layer": [],
        "Source IP": [],
        "Dest IP": [],
        "Source Port": [],
        "Dest Port": [],
        "Packet Length": []
    }
    # df2 contains information about hostile flow
    df2 = pandas.DataFrame(data_dict)
    num2 = 0 # counter of df2
    prediction = nmapModel.predict(X)
    hostile = 0  # this block counts how many 'hostile' packets have been predicted by the model
    safe = 0
    nmap_counter = 0 # counter of test data
    for check in prediction:
        if check == 1:  # change to 0 to force ddos attack
            if num2 == 0:
                # record the first hostile info
                df2.loc[num2] =  df.iloc[nmap_counter]
                num2 += 1
            hostile += 1
        else:
            safe += 1
        
        nmap_counter += 1
    
    print('Nmap Safe Packets Detected: ' + str(safe))
    print("Nmap Hostile Packets Detected: " + str(hostile))
    print("Nmap Suspicious Packets Info: \n")
    print(df2)
    #write to the log file
    if hostile != 0:
        #evil event log
        #event_Logger("flow_log").get_event_log().critical(df2.to_json(orient="records"))
	pass
	#这里用log的话会一直报错
       # print "123"
    # else:
       #Logger("flow_normal_log").get_log().critical(data)
        # pass

    return {
        # 'Prediction': predicted_class
        'Safe_Packets_Detected': str(safe),
        "Hostile_Packets_Detected": str(hostile),
        "Hostile_Packets_Info": df2.to_json(orient="records") # convert dataframe to json
    }

def LiveLabelEncoding(filename, df):  # same as LabelEncoding(), but use for realtime
    df1 = pandas.read_csv(filename, delimiter=',')
    df1 = df1[['Transport Layer', 'Source IP', 'Dest IP', 'Source Port', 'Dest Port',
                       'Attack Length']]
    df1 = pandas.concat([df1, df], axis=0)
    columnsToEncode = list(df1.select_dtypes(include=['category', 'object']))
    print(columnsToEncode)
    le = LabelEncoder()
    for feature in columnsToEncode:
        try:
            df1[feature] = le.fit_transform(df1[feature])
            # print(data[feature])
        except:
            print('error ' + feature)
    return df1

def LiveLabelEncodingNmap(filename, df):  # same as LabelEncoding(), but use for realtime
    df1 = pandas.read_csv(filename, delimiter=',')
    df1 = df1[['Transport Layer', 'Source IP', 'Dest IP', 'Source Port', 'Dest Port',
                       'Packet Length']]
    df1 = pandas.concat([df1, df], axis=0)
    columnsToEncode = list(df1.select_dtypes(include=['category', 'object']))
    print(columnsToEncode)
    le = LabelEncoder()
    for feature in columnsToEncode:
        try:
            df1[feature] = le.fit_transform(df1[feature])
            # print(data[feature])
        except:
            print('error ' + feature)
    return df1


#data = ["{'Attack Length': 0, 'Source IP': u'192.168.3.207', 'Transport Layer': u'udp', 'Source Port':5010, 'Dest Port':5010, 'Dest IP': u'192.168.3.255'}"]
#data[0] = eval(data[0])
#data[0] = json.dumps(data[0])
'''for i in range(len(data)):
        #each = eval(each)
#       data[i] = eval(data[i])
        data[i] = json.dumps((data[i]))
        print(data[i])
'''
data = ['{"Transport Layer": "udp", "Source IP": "192.168.3.207", "Dest IP": "192.168.3.255", "Source Port": 5010, "Dest Port": 5010, "Attack Length": 0}', '{"Transport Layer": "udp", "Source IP": "192.168.3.207", "Dest IP": "192.168.3.255", "Source Port": 5010, "Dest Port": 5010, "Attack Length": 0}', '{"Transport Layer": "udp", "Source IP": "192.168.3.207", "Dest IP": "192.168.3.255", "Source Port": 5010, "Dest Port": 5010, "Attack Length": 0}']*100
data = [{"Attack Length": 0, "Source IP": "121.15.171.82", "Transport Layer": "tcp", "Packet Length": 60, "Source Port": 46946, "Dest Port": 9002, "Dest IP": "192.168.3.50"}]*100

#data[0] = json.dumps(data[0])
