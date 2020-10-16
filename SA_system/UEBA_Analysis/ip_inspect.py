#coding:utf-8
import pandas as pd
import numpy as np
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

def set_count(data, users, counts):
    data['ip_count'] = 0
    data['new_ip_count'] = 0
    data['mac_count'] = 0
    for i in range(len(users)):
        data.loc[data['username'] == users[i], ['ip_count', 'mac_count']] = counts[i]
    return data

def list_user_ips(data):
    data.drop_duplicates('src_ip', inplace=True)
    users = data.loc[:, ['username']].values.tolist()
    ips = data.loc[:, ['src_ip']].values.tolist()
    ip_dict = {}
    for i in range(len(users)):
        if users[i][0] in ip_dict:
            ip_dict[users[i][0]].append(ips[i][0])
        else:
            ip_dict[users[i][0]] = [ips[i][0]]

    return ip_dict

# if __name__ == '__main__':
#     df = load_data(data_path)
#     tmp = df.copy(deep=True)
#     # ------------------统计当日用户使用ip-------------------
#     counts, users = count_ip(tmp)
#     plt.bar(users, counts, align='center')
#     plt.title('User IP usage')
#     plt.ylabel('ip count')
#     plt.xlabel('users')
#     plt.show()
#     # df = set_count(df, users, counts)
#     # print df
#     # ------------------统计过去一月用户常使用ip-------------------
#     # dict = list_user_ips(tmp)
#     # print dict
#     # data = series_to_array(df['online'])
#     # kde_analyze(data)
