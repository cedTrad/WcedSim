import pandas as pd
import numpy as np

pd.set_option('mode.use_inf_as_na', True)

class Preprocessing:
    
    def __init__(self):
        #self.data = data
        self.asset_data = {}
    
    def split_asset(self, data):
        asset_data = {}
        symbols = data.symbol.unique()
        for i, symbol in enumerate(symbols):
            asset_data[symbol] = data[data.symbol == symbol]
        return asset_data
            
    
    def add_features(self, trade):
        trade['gp'] = np.where((trade['status'] == 'open') | ((trade['position'] == 0) & (trade['status'] != 'close')),
                               0, trade.pnl.diff())
        trade['cum_gp'] = trade.gp.cumsum()
        
    
    def pre_preprocess(self, trade = None, portfolio_data = None ):
        trade = trade.copy()
        portfolio_data = portfolio_data.copy()
        if trade is not None:
            try:
                trade.drop(columns = ['key'], inplace = True)
            except:
                pass
            trade.set_index('date', inplace = True)
            trade['value2'] = trade['value'] + trade['out_value']
        
        if portfolio_data is not None:
            try:
                portfolio_data.drop(columns = ['key'], inplace = True)
            except:
                pass
        portfolio_data.set_index('date', inplace = True)
        portfolio_data = portfolio_data.groupby('date').last().copy()
        portfolio_data["rets"] = portfolio_data["capital"].pct_change()
        portfolio_data["cum_rets"] = (portfolio_data["rets"] + 1).cumprod()
        
        return trade, portfolio_data
        
        
        
    def get_signal(self, trade):
        loc = np.where(trade['status'] == 'open')
        entry_point = trade.iloc[loc][['type_', 'status', 'price']]
        
        loc = np.where(trade['status'] == 'close')
        exit_point = trade.iloc[loc][['type_', 'status', 'price']]
        
        return entry_point, exit_point
    
    
    
    
        