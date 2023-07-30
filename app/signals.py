import pandas as pd 

from .strategies.strategy import Momentum, TMM
from .strategies.strategy_ml import Ml


class Signal:
    
    def __init__(self):
        self.strategies_matrix = pd.DataFrame()
        
    
    def update_df(self, data, symbol):
        self.data = data.copy()
        self.symbol = symbol
        self.st_mom = Momentum(data)
        self.st_tmm = TMM(data)
        self.st_ml = Ml(data)
        self.set_params()
        
        
    def set_params(self):
        self.st_tmm.set_params(3, 8, 14)
    
    
    def get_signal(self, bar):
        matrix = {}
        s1 = self.st_mom.run(bar)
        s2 = self.st_tmm.run(bar)
        
        matrix["s1"] = s1
        matrix["s2"] = s2
        matrix["symbol"] = self.symbol
        add = pd.DataFrame(matrix, [bar])
        self.strategies_matrix = pd.concat([self.strategies_matrix, add], ignore_index=True)
        #self.strategies_matrix = self.strategies_matrix.append(add)
        return s2
        
    
    def get_ml_signal(self, bar, model):
        s1 = self.st_ml.run(bar, model)
        return s1
    
    
    
        
    
        