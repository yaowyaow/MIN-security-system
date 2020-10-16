#coding:utf-8
import pandas as pd
import numpy as np
from sklearn.neighbors import KernelDensity
import pickle
import url_cluster
import resource_inspect
from sklearn.model_selection import GridSearchCV
import pymongo


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
    time_process(data)
    # 数据去重
    data.drop_duplicates('online', inplace=True)
    return data

def time_process(df):
    df['Time'] = pd.to_datetime(df['Time'])
    df['online'] = df['Time'].dt.hour + np.random.random(df['Time'].shape[0])

def series_to_array(series):
    try:
        return np.float64(series)
    except ValueError:
        return np.nan

def process_np_array(data):
    sorted_data = data[np.argsort(data)]
    sorted_matrix = sorted_data.reshape(-1, 1)
    return sorted_data, sorted_matrix

def kde_analyze(data):
    sorted_data, fit_data = process_np_array(data)
    grid_param = {
        'bandwidth': [0.5, 0.75, 1]
    }
    print sorted_data.shape
    # kde_grid = GridSearchCV(KernelDensity(kernel="gaussian"), grid_param)
    kde_grid = KernelDensity(kernel="gaussian", bandwidth=0.75)
    # kde = kde_grid.fit(fit_data).best_estimator_
    kde = kde_grid.fit(fit_data)
    return sorted_data.tolist(), np.exp(kde.score_samples(fit_data)).tolist()
    # pickle.dump(kde, open('kde_time.model', 'wb'), protocol=2)
    # plt.title("User online time distribution")
    # plt.xlabel("hours")
    # plt.ylabel("probability")
    # plt.plot(sorted_data, np.exp(kde.score_samples(fit_data)), '-')
    # plt.hist(test_data, facecolor="blue", edgecolor="black", alpha=0.7)
    # plt.show()

def count_abnormal_operations(data, users):
    result = {}
    for user in users:
        if user not in result:
            result[user] = 0
        result[user] = inspect(np.array(data.loc[data['username'] == user, ['online']]))
    return result

def set_time_count(data, dict):
    data['time_count'] = data['Time']
    for i in dict:
        data.loc[data['username'] == i, ['time_count']] = dict[i]
    return data

def get_users(data):
    data.drop_duplicates('username', inplace=True)
    return np.array(data['username'])

def inspect(data):
    kde = pickle.load(open('kde_time.model', 'rb'))
    result = np.exp(kde.score_samples(data))
    return result[result < 0.01].size

if __name__ == '__main__':
    df = load_data(data_path)
    # tmp = df.copy(deep=True)
    # users = get_users(tmp)
    # print df
    # print count_abnormal_operations(df, users)
    # data = df['request'].str.replace('[0-9]*', '')
    # df['request'] = data
    # print url_cluster.count_abnormal_operations(df, users)
    # print resource_inspect.count_abnormal_operations(df, users)
    data = series_to_array(df['online'])
    time, data = kde_analyze(data)
    store = {'time': time, 'data': data}
    print store
    client = connect()
    store_data(store, client, 'login_time')
