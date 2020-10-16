import pandas as pd
import numpy as np
# import main as ma

data_path = './ueba.xlsx'

def load_json(path):
    df = pd.read_excel(path)
    return df

def process_count(df):
    df['Time'] = pd.to_datetime(df['Time'])
    df['online'] = df['Time'].dt.hour + df['Time'].dt.minute / 100
    return df

def count_hourly_flow(df):
    day_count = {}
    day_arr = []
    for i in range(24):
        hour_data = np.array(df.loc[(df['online'] > i) & (df['online'] < i + 1), ['bytes']])
        if hour_data.shape[0] != 0:
            day_count[i] = np.sum(hour_data) * 1.0 / 1024
            day_arr.append(day_count[i])
        else:
            day_count[i] = 0
            day_arr.append(0)

    return day_count, day_arr

def count_weekly_flow(df, dates, users):
    week_arr = []
    week_dict = {}
    for date in dates:
        day_data = df.loc[df['date'] == date, ['bytes', 'online']]
        day_count, day_arr = count_hourly_flow(day_data)
        week_arr.append(day_arr)
    week_arr = np.array(week_arr) / users.shape[0]
    week_arr = np.sum(week_arr, axis=0) / dates.shape[0]
    for i in range(24):
        week_dict[i] = week_arr[i]
	#	week_dict[str(i)] = week_arr[i]
    return week_dict

def count_abnormal_flow(data, users, week):
    result = {}
    for user in users:
        if user not in result:
            result[user] = 0
        test_data = data.loc[data['username'] == user, ['bytes', 'online']]
        user_flow_dict, user_flow_arr = count_hourly_flow(test_data)
        # print user_flow_dict
        result[user] = inspect(week, user_flow_dict)
    return result

def inspect(dict1, dict2):
    res = 0
    for i in range(24):
        if dict2[i] > dict1[i]:
            res += dict2[i] - dict1[i]
    return res

def set_flow_count(data, dict):
    data['abnormal_flow'] = 0
    for i in dict:
        data.loc[data['username'] == i, ['abnormal_flow']] = dict[i]

    return data

'''
df = load_json(data_path)
df = process_count(df)
tmp_df = df.copy(deep=True)
users = ma.get_users(tmp_df)
tmp_df = df.copy(deep=True)
dates = ma.get_dates(tmp_df)
week_dict = count_weekly_flow(df, dates, users)
print week_dict
client = ma.connect()
ma.store_data(week_dict, client, 'flow_usage')
'''
