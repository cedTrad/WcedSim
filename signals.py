from strategies.strategy import Momentum
#from strategies.strategy_ml import Ml


class Signal:
    
    def __init__(self, data):
        self.data = data.copy()
        self.st_mom = Momentum(self.data)
        #self.st_ml = Ml(data)
    
    def get_signal(self, bar):
        return self.st_mom.run(bar)
    
    def get_ml_signal(self, bar, model):
        return self.st_ml.run(bar, model)
    
    
    
        
    
        