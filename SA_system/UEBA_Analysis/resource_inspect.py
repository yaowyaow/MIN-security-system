#coding:utf-8
import pandas as pd
import numpy as np
import string
from sklearn.neighbors import KernelDensity
from sklearn.model_selection import GridSearchCV


data_path = 'ueba.xlsx'

def load_data(path):
    data = pd.read_excel(path)
    return data

def count_ip(data):
    # 数据去重
    data.drop_duplicates('src_ip', inplace=True)
    counts = data['username'].value_counts()
    users = data['username'].value_counts().index
    return counts, users

def set_file_count(data, dict):
    data['file_count'] = data['command']
    for i in dict:
        data.loc[data['username'] == i, ['file_count']] = dict[i]
    return data

def count_abnormal_operations(data, users):
    result = {}
    for user in users:
        if user not in result:
            result[user] = 0
        test_data = data.loc[data['username'] == user, ['command']]
        test_data = np.array(test_data).reshape(1, -1)
        # result[user] = inspect(test_data[0])
        result[user] = inspect(test_data[0])
    return result

def inspect(data):
    tmp = 0
    for i in data:
        if i.find('file') or i.find('File'):
            tmp += 1
    return tmp

# if __name__ == '__main__':
#     df = load_data(data_path)
#     tmp = df.copy(deep=True)
#     # ------------------统计当日用户使用ip-------------------
#     counts, users = count_ip(tmp)
