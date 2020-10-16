import pandas as pd
import numpy as np
from sklearn.ensemble import IsolationForest
from sklearn import svm
from sklearn.neighbors import LocalOutlierFactor
import pickle

def isolation_score(data):
    iForest = pickle.load(open('forest.model', 'rb'))
    return iForest.score_samples(data)

def local_outlier_score(data):
    clf = pickle.load(open('lof.model', 'rb'))
    clf.predict(data)
    return clf.negative_outlier_factor_

def one_class_svm_score(data):
    clf = pickle.load(open('oneclass.model', 'rb'))
    return clf.score_samples(data)

def train_isolation(data):
    iForest = IsolationForest(n_estimators=500,random_state=75,behaviour='new')
    iForest.fit(data)
    pickle.dump(iForest, open('forest.model', 'wb'), protocol=2)

def train_local_outlier(data):
    clf = LocalOutlierFactor(n_neighbors=20, novelty=True)
    clf.fit(data)
    pickle.dump(clf, open('lof.model', 'wb'), protocol=2)

def train_one_class(data):
    clf = svm.OneClassSVM(gamma='auto').fit(data)
    pickle.dump(clf, open('oneclass.model', 'wb'), protocol=2)

def train(data):
    train_isolation(data)
    train_local_outlier(data)
    train_one_class(data)

def score(data):
    print isolation_score(data)
    print local_outlier_score(data)
    print one_class_svm_score(data)
