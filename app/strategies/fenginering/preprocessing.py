import pandas as pd
import numpy as np
import itertools

from sklearn.preprocessing import FunctionTransformer
from sklearn.model_selection import ParameterGrid
from sklearn.pipeline import Pipeline, FeatureUnion, make_pipeline


class Crossover:
    
    
    def __init__(self, data):
        self.data = data.copy()
        self.names = []
        self.steps = []
    
    def add_colname(self, funct, params):
        for i, param in enumerate(params):
            if isinstance(param, dict):
                cols = funct(self.data, **param).columns.to_list()
            else:
                cols = funct(self.data, param).name
                cols = [cols]
            self.names.extend(cols)
    
    
    def one_params(self, data, params, funct):
        df = pd.DataFrame()
        for param in params:
            df = pd.concat([df, funct(data, param)], axis = 1)
        return df
    
    
    def set_stransformer(self, funct, params):
        transformer = FunctionTransformer(self.one_params, kw_args = {"params" : params, "funct" : funct})
        self.add_transformer(name = funct.__name__, transformer = transformer)
        return transformer
    
    def add_transformer(self, name, transformer):
        step = (name, transformer)
        self.steps.append(step)
    
    
    def ma(self, funct, params):
        transformer = self.set_stransformer(funct, params)
        self.add_colname(funct, params)
        
        data = transformer.fit_transform(self.data).copy()
        data_ = {}
        
        variable = list(itertools.combinations(self.names, 2))
        for couple in variable:
            name = ""
            i = 0
            name = couple[i]+"_" + couple[i+1]
            data_[name] = np.where(data[couple[i]] < data[couple[i+1]], 1, 0)
            data_[name+'dist'] = (data[couple[i+1]] + data[couple[i]]) / data[couple[i]]
        
        for col in self.names:
            data_[name+"_c"] = (data[couple[i]] + self.data['close']) / self.data['close']
        
        
        data_ = pd.DataFrame(data_)
        
        #data.drop(columns = self.names, inplace = True)   
        data_.dropna(inplace = True)    
        self.names = []
        
        return data_
    
    def macd(self):
        ""
        

def h_l(data):
    X = (data['high'] - data['low']) / data['low']
    X.name = 'h-l'
    return X


class Scale:
    
    def __init__(self, data):
        self.data = data.copy()
    
    
    def h_l(self):
        self.data['h_l'] = (self.data['high'] - self.data['low']) / self.data['low']
    
    
    def drop(self):
        self.data.drop(columns = ['open', 'high', 'low', 'close', 'volume'], inplace = True)
    
    def transform(self):
        self.h_l()
        
        self.drop()
        
        return self.data