import numpy as np
import pandas as pd
import itertools


def get_classification_target(data):
    data = data.copy()
    data['returns'] = data["close"].pct_change()
    data['target'] = data['returns'].shift(-1)
    data['target'] = np.where(data['target'] > 0, 1, 0)
    return data['target']


def get_regression_target(data):
    data = data.copy()
    data['returns'] = data["close"].pct_change()
    data['target'] = data['returns'].shift(-1)
    return data['target']


def crossover(df):
    data = df.copy()
    colnames = data.columns
    variables = list(itertools.combinations(colnames, 2))
    
    for couple in variables:
        i = 0
        name = couple[i]+"_"+couple[i+1]
        data[name] = np.where(data[couple[i]] < data[couple[i+1]], 1, 0)
        
        name = couple[i+1]+"_"+couple[i]
        data[name] = np.where(data[couple[i]] > data[couple[i+1]], 1, 0)
    return data.drop(columns = colnames)


def crossover_dist(df):
    data = df.copy()
    colnames = data.columns
    variables = list(itertools.combinations(colnames, 2))
    
    for couple in variables:
        i = 0
        name = couple[i]+"_"+couple[i+1]
        data[name+'dist'] = (data[couple[i+1]] + data[couple[i]]) / data[couple[i]]
        
    return data.drop(columns = colnames)


def set_timeframe(data, base, interval):
    data = data.groupeby(interval).last()

