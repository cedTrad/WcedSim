class Momentum:
    
    def __init__(self, data):
        self.data = data.copy()
        
    def preprocess(self):
        self.data['mom'] = self.data["close"].pct_change().rolling(3).mean()
    
        
    def run(self, bar):
        self.preprocess()
        
        if self.data["mom"].iloc[bar] > 0:
            return "LONG"
        elif self.data["mom"].iloc[bar] < 0:
            return "SHORT"
        else:
            return None