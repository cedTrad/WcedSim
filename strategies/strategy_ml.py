from fenginering.indicator import *
from fenginering.transformer import *

import joblib


lag_ret_list = [1, 3, 5, 9, 15, 30]
ema_list = [3, 9, 15]
rsi_list = [10, 14, 20]


def transform(data):
    Indicators = MakeIndicator(data)
    Indicators.set_stransformer(lag_returns, lag_ret_list)
    Indicators.set_stransformer(rsi, rsi_list)
    return Indicators.transform()


class Ml:
    
    def __init__(self, data):
        self.data = data.copy()
        
    def get_model(self, model):
        return joblib.load(f'ml/model/{model}.joblib')
    
    def run(self, bar, model= "model_1d"):
        
        self.data = transform(self.data)
        x = self.data.iloc[bar].values.reshape([1, -1])
        
        model = self.get_model(model)
        side = model.predict(x)[0]
        proba = model.predict_proba(x)[:,1][0]
        
        if proba > 0.7:
            return "LONG"
        elif proba < 0.3:
            return "SHORT"
        else:
            return None