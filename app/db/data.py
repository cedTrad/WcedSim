import pandas as pd
import numpy as np
import sqlalchemy

from .ohlc import update_data, asset_binance

class connect_db:
    
    def __init__(self, name : str, interval = "1d", path = "C:/Users/cc/Desktop/CedAlgo/database/"):
        self.name = name
        self.interval = interval
        self.path = path
        self.engine = sqlalchemy.create_engine('sqlite:///'+self.path+self.name+"_"+self.interval+".db")
    
    def get_data(self, symbol , start = '2017', end = '2023'):
        data = pd.read_sql(symbol+"USDT", self.engine)
        data.set_index('time' , inplace=True)
        data['volume'] = pd.to_numeric(data['volume'])
        data = data[['open', 'high', 'low' , 'close' , 'volume']]
        data = data.loc[start:end].copy()
        return data
    
    
    def update(self, assets = None, interval = "1d"):
        if assets is None:
            try:
                all_assets = asset_binance()
                update_data(all_assets, interval)
            except:
                pass
        else:
            update_data(assets, interval)
    

