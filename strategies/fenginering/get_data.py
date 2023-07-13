import pandas as pd
import numpy as np
import sqlalchemy


path = "C:/Users/cc/Desktop/CedAlgo/database/"

def get_data(Id , interval):
    engine = sqlalchemy.create_engine('sqlite:///'+path+'database_{}.db'.format(interval))
    
    data = pd.read_sql(Id+'USDT' ,engine)
    data.set_index('time' , inplace=True)
    data['volume'] = pd.to_numeric(data['volume'])
    data = data[['open', 'high', 'low' , 'close' , 'volume', 'symbol']]
    return data


def get_multi_data(interval, table = 'close'):
    engine = sqlalchemy.create_engine('sqlite:///'+path+'database_multi_{}.db'.format(interval))
    data = pd.read_sql(table ,engine)
    data.set_index('time', inplace = True)
    data.dropna(inplace = True)
    return data


