import pandas as pd
import numpy as np
import sqlalchemy


class connect_db:
    
    def __init__(self, name : str, path = "C:/Users/cc/Desktop/CedAlgo/database/"):
        self.name = name
        self.path = path
        self.engine = sqlalchemy.create_engine('sqlite:///'+self.path+self.name)
    
    def get_data(self, symbol , start = '2017', end = '2023'):
        data = pd.read_sql(symbol+"USDT", self.engine)
        data.set_index('time' , inplace=True)
        data['volume'] = pd.to_numeric(data['volume'])
        data = data[['open', 'high', 'low' , 'close' , 'volume']]
        self.data = data.loc[start:end].copy()
        return self.data
    
    def get_m_data(self, symbols):
        ""
    
