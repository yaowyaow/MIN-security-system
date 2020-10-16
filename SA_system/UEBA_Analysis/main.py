#coding:utf-8
#import ip_inspect
#import ensemble_analysis
#import kde_time
#import resource_inspect
#import url_cluster
import numpy as np
import pandas as pd
from sklearn.preprocessing import normalize
#import flow_inspect
import pymongo
import json

data_path = 'ueba.xlsx'
'''
 建立mongodb连接
'''
def connect():
    client = pymongo.MongoClient('localhost', 27017)
    return client

'''
 将预测数据写入 mongodb
'''
def store_data(data, client, name):
    db = client['packet_flow']
    try:
        if db[name].insert(data):
            print 'success'
    except Exception:
        print 'failure'


def load_data(path):
    data = pd.read_excel(path)
    kde_time.time_process(data)
    # 数据去重
    data.drop_duplicates('online', inplace=True)
    return data

def get_users(data):
    data.drop_duplicates('username', inplace=True)
    return np.array(data['username'])

def get_dates(data):
    data.drop_duplicates('date', inplace=True)
    return np.array(data['date'])

def mid_to_max(data, best):
    M = np.max(data - best)
    data = 1 - (data - best) * 1.0 / (M + 0.01)
    return data

def interval_to_max(data, low, high):
    M = max(low - np.min(data), np.max(data) - high)
    values = []
    for i in data:
        if i < low:
            values.append(1 - (low - i) * 1.0 / M)
        elif i > high:
            values.append(1 - (i - high) * 1.0 / M)
        else:
            values.append(1)
    return np.array(values)

def topsis(mt):
    max_vec = np.max(mt, axis=0).reshape(1, -1)
    min_vec = np.min(mt, axis=0).reshape(1, -1)
    max_vec = np.tile(max_vec, (mt.shape[0], 1))
    min_vec = np.tile(min_vec, (mt.shape[0], 1))
    max_mt = mt - max_vec
    min_mt = mt - min_vec
    max_mt = np.power(max_mt, 2)
    min_mt = np.power(min_mt, 2)
    max_sum = np.sum(max_mt, axis=1)
    min_sum = np.sum(min_mt, axis=1)
    max_sum = np.sqrt(max_sum)
    min_sum = np.sqrt(min_sum)
    res = min_sum / (max_sum + min_sum)
    return res

def train(date):
    data = load_data(data_path)
    tmp = data.copy(deep=True)
    users = get_users(tmp)
    tmp = data.copy(deep=True)
    dates = get_dates(tmp)
    week_dict = flow_inspect.count_weekly_flow(data, dates, users)
    # print week_dict
    data = data.loc[data['date'] == date]
    # ---------------------
    kde_time.set_time_count(data, kde_time.count_abnormal_operations(data, users))
    # ---------------------
    url_cluster.set_url_count(data, url_cluster.count_abnormal_operations(data, users))
    # --------------------
    resource_inspect.set_file_count(data, resource_inspect.count_abnormal_operations(data, users))
    # --------------------
    tmp = data.copy(deep=True)
    counts, users2 = ip_inspect.count_ip(tmp)
    ip_inspect.set_count(data, users2, counts)
    # --------------------
    flow_inspect.set_flow_count(data, flow_inspect.count_abnormal_flow(data, users, week_dict))
    data.drop_duplicates('username', inplace=True)
    res = data.loc[:, ['username','ip_count', 'url_count', 'time_count', 'file_count', 'abnormal_flow', 'date', 'new_ip_count', 'mac_count']]
    data['ip_count'] = mid_to_max(np.array(data.loc[:, ['ip_count']]).reshape(1, -1)[0], 1)
    data['new_ip_count'] = mid_to_max(np.array(data.loc[:, ['new_ip_count']]).reshape(1, -1)[0], 1)
    data['mac_count'] = mid_to_max(np.array(data.loc[:, ['mac_count']]).reshape(1, -1)[0], 1)
    data['time_count'] = mid_to_max(np.array(data.loc[:, ['time_count']]).reshape(1, -1)[0], 0)
    data['url_count'] = mid_to_max(np.array(data.loc[:, ['url_count']]).reshape(1, -1)[0], 0)
    data['file_count'] = interval_to_max(np.array(data.loc[:, ['file_count']]).reshape(1, -1)[0], 0, 1000)
    data['abnormal_flow'] = mid_to_max(np.array(data.loc[:, ['abnormal_flow']]).reshape(1, -1)[0], 0)
    train_data = np.array(data.loc[:, ['ip_count', 'new_ip_count', 'mac_count', 'url_count', 'time_count', 'file_count', 'abnormal_flow']])
    train_data = normalize(train_data, axis=0, norm='max')
    result = np.sqrt(topsis(train_data) * 100) * 10
    res['score'] = result
    return res
'''
if __name__ == '__main__':
    client = connect()
    dates = ['2020-08-07', '2020-08-08', '2020-08-09', '2020-08-10', '2020-08-11', '2020-08-12', '2020-08-13']
    for date in dates:
        df = train(date)
        ueba_data = json.loads(df.to_json(orient = 'records'))
        print ueba_data
        for data in ueba_data:
            data['date'] = date
            store_data(data, client, 'ueba_data')
'''

