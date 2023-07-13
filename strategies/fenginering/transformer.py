import pandas as pd
from sklearn.preprocessing import FunctionTransformer
from sklearn.model_selection import ParameterGrid

from sklearn.pipeline import Pipeline, FeatureUnion, make_pipeline


def param_grid(params):
    return list(ParameterGrid(params))

def sin_transformer(period):
    return FunctionTransformer(lambda x : np.sin(x / period*2*np.pi))

def cos_transformer(period):
    return FunctionTransformer(lambda x : np.cos(x / period*2*np.pi))


class MakeIndicator:
    
    def __init__(self, data):
        self.data = data.copy()
        self.names = ['open', 'high', 'low', 'close', 'volume']
        self.index = data.index
        self.steps = [("ohlcv", FunctionTransformer(lambda x : x[['open', 'high', 'low', 'close', 'volume',]]))]
        #self.steps = []
    
    
    def one_params(self, data, params, funct):
        df = pd.DataFrame()
        for param in params:
            df = pd.concat([df, funct(data, param)], axis = 1)
        return df
    
    def multi_params(self, data, params_grid, funct):
        df = pd.DataFrame()
        for param in params_grid:
            df = pd.concat([df, funct(data, **param)], axis = 1)
        return df
    
    def param_grid(self, params):
        return list(ParameterGrid(params))
    
    
    def add_colname(self, funct, params):
        for i, param in enumerate(params):
            if isinstance(param, dict):
                cols = funct(self.data, **param).columns.to_list()
            else:
                cols = funct(self.data, param).name
                cols = [cols]
            for j in range(len(cols)):
                cols[j] = cols[j] + "_" + str(i)
            self.names.extend(cols)
                
            
    def set_stransformer(self, funct, params):
        self.add_colname(funct, params)
        transformer = FunctionTransformer(self.one_params, kw_args = {"params" : params, "funct" : funct})
        self.add_transformer(name = funct.__name__, transformer = transformer)
        #return transformer
        
    def set_mtransformer(self, funct, params):
        params = self.param_grid(params)
        self.add_colname(funct, params)
        transformer = FunctionTransformer(self.multi_params, kw_args = {"params_grid" : params, "funct" : funct})
        self.add_transformer(name = funct.__name__, transformer = transformer)
        #return transformer
    
    
    def add_transformer(self, name, transformer):
        step = (name, transformer)
        self.steps.append(step)
    
    
    def makeUnion(self):
        union = FeatureUnion(
            self.steps
        )
        return union
    
    
    def transform(self):
        union = self.makeUnion()
        
        data = union.fit_transform(self.data)
        data = pd.DataFrame(data, columns = self.names, index = self.index)
        self.na_count = data.isna().sum().max()
        
        data.dropna(inplace = True)
        
        return data
    

