import pandas as pd
import sqlalchemy
import datetime
#from binance.client import Client
import time
import pytz
from IPython.display import clear_output


path = "C:/Users/cc/Desktop/CedAlgo/database/"
def createEngine(interval = '1h'):
    return sqlalchemy.create_engine('sqlite:///'+path+'database_{}.db'.format(interval))


def tableName(engine):
    ins = sqlalchemy.inspect(engine)
    return ins.get_table_names()

# Structurer les donnees
def structureData(X, symbol):
    data = X
    data.columns = ['time','open', 'high', 'low', 'close', 'volume', 'close_time', 'qav', 'num_trades', 'taker_base_vol', 'taker_quote_vol','is_best_match']
    data['time'] = pd.to_datetime(data['time'], unit = 'ms')
    data['close'] = pd.to_numeric(data['close'])
    data['open'] = pd.to_numeric(data['open'])
    data['high'] = pd.to_numeric(data['high'])
    data['low'] = pd.to_numeric(data['low'])
    data['volume'] = pd.to_numeric(data['volume'])
    data['symbol'] = symbol
    return data


#  Importation data
def LoadData(symbol, start, interval):
    while 1 :
        try:
            client = Client()
            break
        except:
            "error client "
            
    X = pd.DataFrame(client.get_historical_klines(symbol=symbol, start_str=start, interval=interval))
    data =  structureData(X, symbol)
    engine = createEngine(interval)
    try:
        data.to_sql(symbol, engine)
    except:
        "Erreur inconnu au niveau de loadData "
    
    

def Load_data(token, interval , start):
    engine = createEngine(interval)
    pairExistant = tableName(engine)
    symbol = token+'USDT'
    
    if symbol in pairExistant:
        data = pd.read_sql(symbol, engine)
        if interval == '1d':
            lastDate = data.iloc[-1]['time'] + datetime.timedelta(days = 1)
        elif interval == '1h':
            lastDate = data.iloc[-1]['time'] + datetime.timedelta(hours = 1)
            
        Start = "{}-{}-{} {}:{}:{}".format(lastDate.year, lastDate.month, lastDate.day, lastDate.hour, lastDate.minute, lastDate.second)
        utc = pytz.utc
        today = datetime.datetime.now(utc)
        today = datetime.datetime(today.year , today.month , today.day , today.hour)
        diff = today - lastDate
        days = diff.days
        hour = diff.seconds/3600
        
        if (days == 0 and hour > 0) or (days > 0):
            i = 0
            while i<50:
                try :
                    client = Client()
                    break
                except:
                    "error client"
            
            X = client.get_historical_klines(symbol = symbol, start_str = Start , interval = interval)
            X = pd.DataFrame(X)
            data_add = structureData(X , symbol)
            data_add.to_sql(symbol , engine , if_exists = 'append' , index = True) 
            print('     Updated     ')
        elif (days == 0) and (hour == today.hour) :
            print('last : ',data['time'][-1])
            print("Already updated")
        else:
            "Please , try later"
            print(f"{token} already update , try later for a update")  
    else:
        LoadData(symbol , start , interval)
        print("{token} successful load")   




def update_data(assets ,interval):
    i= 1 ; n = len(assets)
    begin = '1 Jan, 2017'
    fail = []
    for token in assets:
        clear_output(wait = True)
        print(f"numero : {i} / {n} \n token : {token}")
        i += 1
        try:
            Load_data(token , interval , begin)
            time.sleep(0.1)
        except:
            fail.append(token)
    print("loading fail for ... : ",fail)
    

def asset_binance():
    pair = [] ; coins = [] ; quotes = []
    while 1:
        try:
            client = Client()
            exchange_info = client.get_exchange_info()
            break
        except:
            "404"            
    for s in exchange_info['symbols']:
        coins.append(s['baseAsset'])
    coins = list(set(coins))
    return coins


