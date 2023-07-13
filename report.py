import pandas as pd
import numpy as np

from sqlalchemy import create_engine

from data import connect_db
from preprocessing import Preprocessing
from plot import *

from evaluation.metric import Metric

class Report:
    
    def __init__(self, name = 'w'):
        self.name = 'w'
        self.symbols = []
        self.assets = {}
        self.preprocessing = Preprocessing()
    
    def database(self):
        self.db = connect_db("database_1h.db")
        self.engine = create_engine(f"sqlite:///database/data.db")
    
    
    def get_data(self, data = None, portfolio_data = None):
        self.database()
        if data is None:
            self.data = pd.read_sql('trades', self.engine)
        else:
            self.data = data
            
        if portfolio_data is None:
            self.portfolio_data = pd.read_sql('portfolio_tab', self.engine)
        else:
            self.portfolio_data = portfolio_data
            
        self.symbols = list(self.data.symbol.unique())
        self.preprocessing.pre_preprocess(self.data)
        self.assets_data = self.preprocessing.split_asset(self.data)
        self.metrics = Metric(data = self.assets_data)
    
    def features(self, data):
        self.preprocessing.add_features(data)
        
    
    def run(self, data = None, portfolio_data = None):
        # data + pre_processing
        self.get_data(data, portfolio_data)
        
        # add feature for viz
        for symbol in self.symbols:
            df = self.assets_data[symbol]
            self.features(df)
            
        self.metrics.KPI()
        
    
    def viz_asset(self, data, asset, portfolio):
        entry_point , exit_point = self.preprocessing.get_signal(asset)
        
        fig = subplots(nb_rows=3, nb_cols=1, row_heights=[0.2, 0.6, 0.2])
        
        add_line(fig=fig, col=1, row=1, data=asset, feature='pnl_pct', name='pnl_pct')
        add_bar(fig=fig, col=1, row=1, data=asset, name='pnl_pct')
        add_second_y(fig=fig, col=1, row=1, data=asset, name='position')
        
        plot_candle(fig=fig, col=1, row=2, data=data, symbol='ohlc')
        signal_point(fig, col=1, row=2, x = entry_point.index, y = entry_point.price, name='in', marker=(5, 10, 'blue'))
        signal_point(fig, col=1, row=2, x = exit_point.index, y = exit_point.price, name='out', marker=(6, 10, 'black'))
        color_trades(fig=fig, col=1, row=2, entry=entry_point, exit=exit_point, opacity=0.1)
        
        add_line(fig=fig, col=1, row=3, data=asset, feature='cum_gp', name='cum_gp')
        
        return fig
    
    def viz_portfolio(self, portfolio):
        fig = subplots(nb_rows=3, nb_cols=1, row_heights=[0.6, 0.2, 0.2])
        
        add_line(fig = fig, col=1, row=1, data=portfolio, feature='capital', name='capital')
        add_line(fig = fig, col=1, row=2, data=portfolio, feature='safe_value', name='safe_value')
        add_line(fig = fig, col=1, row=3, data=portfolio, feature='risk_value', name='risk_value')
        
        return fig
    
    
    def plot_asset(self, symbol):
        asset = symbol
        data = self.db.get_data(symbol)
        data = data.loc['2023' : '2023']
        
        fig = self.viz_asset(data, self.assets_data[f'{asset}'], self.portfolio_data)
        fig.update_layout(height = 1000 , width =1500)
        return fig
        
    
        
    def plot(self, feature):
        
        portfolio = self.portfolio_data
        try:
            portfolio.set_index("date", inplace = True)
        except KeyError:
            pass
        rows = len(self.symbols)
        
        fig = subplots2(nb_rows=rows+1, nb_cols=1)
        
        for i, symbol in enumerate(self.symbols):
            data = self.assets_data[symbol]            
            add_line(fig = fig, col=1, row=i+1, data=data, feature = feature, name=f'{symbol}')
        
        add_line(fig = fig, col=1, row=rows+1, data=portfolio, feature='capital', name='capital')
        
        fig.update_layout(height = 350 , width = 800,
                          margin = {'t':0, 'b':0, 'l':0})
        
        return fig
        
    
    def plot_portfolio(self):
        fig = self.viz_portfolio(self.portfolio_data)
        fig.update_layout(height = 700 , width = 1200)
        return fig
        
        
    
    