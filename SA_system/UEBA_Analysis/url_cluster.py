import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
import pandas as pd
from sklearn import svm
from string import digits
import pickle

data_path = 'ueba.xlsx'
n = 3

def load_data(path):
    data = pd.read_excel(path)
    return data['request'].str.replace('[0-9]*', '')

def series_to_array(series):
    try:
        return np.array(series)
    except ValueError:
        return np.nan

# tokenizer function, this will make 3 grams of each query
def get_ngrams(query):
    tempQuery = str(query)
    ngrams = []
    for i in range(0, len(tempQuery)-n):
        ngrams.append(tempQuery[i:i+n])
    return ngrams

def getTransformer():
    data = load_data(data_path)
    data = series_to_array(data)
    vectorizer = TfidfVectorizer(tokenizer=get_ngrams)
    vec = vectorizer.fit(data)
    return vec

def train(data):
    vec = getTransformer()
    X_train = vec.transform(data)
    clf = svm.OneClassSVM(nu=0.02, kernel="rbf", gamma=0.05)
    clf.fit(X_train)
    pickle.dump(clf, open('url_cluster.model', 'wb'), protocol=2)
    y_predict = clf.predict(X_train)
    n_error = y_predict[y_predict == -1].size
    print n_error

def count_abnormal_operations(data, users):
    new_data = data['request'].str.replace('[0-9]*', '')
    data['request'] = new_data
    result = {}
    for user in users:
        if user not in result:
            result[user] = 0
        test_data = data.loc[data['username'] == user, ['request']]
        test_data = np.array(test_data).reshape(1, -1)
        result[user] = inspect(test_data[0])
    return result

def set_url_count(data, dict):
    data['url_count'] = data['request']
    for i in dict:
        data.loc[data['username'] == i, ['url_count']] = dict[i]
    return data

def inspect(data):
    vec = getTransformer()
    X_train = vec.transform(data)
    clf = pickle.load(open('url_cluster.model', 'rb'))
    result = clf.predict(X_train)
    return result[result == -1].size

# if __name__ == '__main__':
#     data = load_data(data_path)
#     data = series_to_array(data)
#     train(data)
