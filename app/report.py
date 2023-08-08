import pandas as pd
import numpy as np
import datetime

from sqlalchemy import create_engine

from .db.data import connect_db
from .preprocessing import Preprocessing
from .plot import *
from .pnl_analysis import PNL

from .evaluation.metric import Metric



class Report:
    
    def __init__(self, name = 'w', interval = "1d", start = "", end = "",
                 db_trades = "simulation_"):
        self.name = 'w'
        self.interval = interval
        self.start = start
        self.end = end
        self.db = connect_db(name = "database", interval = self.interval)
        self.engine = create_engine(f"sqlite:///data/{db_trades}.db")
        
        self.symbols = []
        self.assets = {}
        self.preprocessing = Preprocessing()
        self.pnl = PNL(db_trades = db_trades)
    
    
    def get_data(self, data = None, portfolio_data = None, metrics_data = None):
        if data is None:
            self.data = pd.read_sql('trades', self.engine)
        else:
            self.data = data
            
        if portfolio_data is None:
            self.portfolio_data = pd.read_sql('portfolio_tab', self.engine)
        else:
            self.portfolio_data = portfolio_data
            
        self.symbols = list(self.data.symbol.unique())
        self.data, self.portfolio_data = self.preprocessing.pre_preprocess(trade = self.data, portfolio_data = self.portfolio_data)
        self.assets_data = self.preprocessing.split_asset(self.data)
        self.pnl.get_trades(assets_data = self.assets_data)
        self.p_evalutation = PEvalutation(self.portfolio_data)
    

    def run(self, data = None, portfolio_data = None):
        # data + pre_processing
        self.get_data(data, portfolio_data)
        
        # add feature for viz
        for symbol in self.symbols:
            df = self.assets_data[symbol]
            self.preprocessing.add_features(df["data"])
            self.preprocessing.recovery_per_trade(df["data"])
            self.preprocessing.add_features(df["long"])
            self.preprocessing.add_features(df["short"])
        self.pnl.run()
        self.pnl.report(self.engine)
        
    
    def viz_cppi(self, fig, data, floor, cushion):
        add_line(fig, col=None, row=None, data=data, feature=feature, name="floor")
        add_line(fig, col=None, row=None, data=data, feature=feature, name="cushion")
        
    
    def viz_asset(self, data, asset, portfolio):
        entry_point , exit_point = self.preprocessing.get_signal(asset)
        fig = subplots(nb_rows=3, nb_cols=1, row_heights=[0.2, 0.6, 0.2])
        
        add_line(fig=fig, col=1, row=1, data=asset, feature='rets', name='return')
        #add_bar(fig=fig, col=1, row=1, data=asset, feature='pnl_pct', name='pnl_pct')
        add_second_y(fig=fig, col=1, row=1, data=asset, name='position')
        
        plot_candle(fig=fig, col=1, row=2, data=data, symbol='ohlc')
        signal_point(fig, col=1, row=2, x = entry_point.index, y = entry_point.price, name='in', marker=(5, 10, 'blue'))
        signal_point(fig, col=1, row=2, x = exit_point.index, y = exit_point.price, name='out', marker=(6, 10, 'black'))
        color_trades(fig=fig, col=1, row=2, entry=entry_point, exit=exit_point, opacity=0.1)
        
        add_bar(fig=fig, col=1, row=3, data=asset, feature='pnl', name='pnl')
        add_second_y(fig=fig, col=1, row=3, data=asset, name='pnl_pct')
        return fig
    
    
    def viz_portfolio(self, portfolio,  pct = True):
        fig = subplots2(nb_rows=2, nb_cols=1, row_heights=[0.2, 0.8])
        
        add_line(fig = fig, col=1, row=1, data=portfolio, feature='cum_gp', name='cum_gp', color = "blue")
        
        add_line(fig = fig, col=1, row=2, data=portfolio, feature='capital', name='capital', color = "blue")
        add_bar(fig = fig, col=1, row=2, data=portfolio, feature='available_value', name='available_value', color = "green")
        add_bar(fig = fig, col=1, row=2, data=portfolio, feature='risk_value', name='risk_value', color = "red")
        add_hline(fig = fig, col=1, row=2, data=portfolio, feature='floor_value', color = "white")
        
        #colors = np.where(portfolio["rets"]>0, "green", "red")
        #add_bar(fig = fig, col=1, row=3, data=portfolio, feature='rets', name='return', color = colors)
        #add_line(fig = fig, col=1, row=3, data=portfolio, feature='rets', name='return', color = colors)
        return fig
    
    
    def viz_portfolio_dist(self, pct = True):
        fig = go.Figure()
        if not pct:
            add_hist(fig=fig, data=self.portfolio_data, feature="gp", name = "gp" )
        else:
            add_hist(fig=fig, data=self.portfolio_data, feature="rets", name = "returns" )
        return fig
        #n=
    
    
    def plot_asset(self, symbol):
        asset = symbol
        start = self.data.index[0]
        end = self.data.index[-1]
        
        data = self.db.get_data(symbol, start = start, end = end)
        data = data.loc[start : end]
        
        fig = self.viz_asset(data, self.assets_data[f'{asset}']["data"], self.portfolio_data)
        fig.update_layout(height = 1000 , width =1500,
                          legend = dict(orientation="h",
                                        yanchor="bottom", y=1,
                                        xanchor="right", x=0.5),
                          margin = {'t':0, 'b':0, 'l':10, 'r':0}
                          )
        return fig
        
           
    def plot(self, feature, bar = False):
        
        portfolio = self.portfolio_data
        try:
            portfolio.set_index("date", inplace = True)
        except KeyError:
            pass
        rows = len(self.symbols)
        
        fig = subplots2(nb_rows=rows+1, nb_cols=1)
        
        for i, symbol in enumerate(self.symbols):
            data = self.assets_data[symbol]["data"]
            if bar:
                add_bar(fig = fig, col=1, row=i+1, data=data, feature = feature, name=f'{symbol}')
            else:
                add_line(fig = fig, col=1, row=i+1, data=data, feature = feature, name=f'{symbol}')
                
        add_line(fig = fig, col=1, row=rows+1, data=portfolio, feature='capital', name='capital')
        fig.update_layout(height = 500 , width = 1000,
                          legend = dict(orientation="h",
                                        yanchor="bottom", y=1,
                                        xanchor="right", x=0.5),
                          margin = {'t':0, 'b':0, 'l':10, 'r':0}
                          )
        
        return fig
    
    
    def plot_portfolio(self):
        fig = self.viz_portfolio(self.portfolio_data)
        fig.update_layout(height = 600 , width = 1200,
                          barmode = 'stack',
                          legend = dict(orientation="h",
                                        yanchor="bottom", y=1,
                                        xanchor="right", x=0.5),
                          modebar_remove=['zoom', 'pan'],
                          margin = {'t':0, 'b':0, 'l':10, 'r':0}
                          )
        return fig
        #n=
        
    def plot_cppi(self):
        fig = subplots2(nb_rows=2, nb_cols=1, row_heights=[0.7, 0.3])
        add_line(fig = fig, col=1, row=1, data = self.portfolio_data, feature='capital', name='capital', color = "blue")
        add_line(fig = fig, col=1, row=1, data = self.portfolio_data, feature='floor_value', name='floor_value', color = "red")
        
        add_line(fig = fig, col=1, row=2, data = self.portfolio_data, feature='risky_w', name='risk_w', color = "blue")
        
        fig.update_layout(height = 600 , width = 1000,
                          legend = dict(orientation="h",
                                        yanchor="bottom", y=1,
                                        xanchor="right", x=0.5),
                          margin = {'t':0, 'b':0, 'l':10, 'r':0}
                          )
        return fig
    
    def plot_metric(self, feature):
        data = self.metrics.df
        fig = go.Figure()
        add_line(fig = fig, col=None, row=None, data=data, feature=feature, name=feature, color="blue")
        fig.update_layout(height = 600 , width = 1000,
                          legend = dict(orientation="h",
                                        yanchor="bottom", y=1,
                                        xanchor="right", x=0.5),
                          margin = {'t':0, 'b':0, 'l':10, 'r':0}
                          )
        return fig
    

#n=
class PEvalutation:
    
    def __init__(self, portfolio_data):
        self.portfolio_data = portfolio_data
    
    def recovery_curve(self):
        fig = go.Figure()
    
    def plot(self):
        #fig = go.Figure()
        fig = subplots2(nb_rows=2, nb_cols=1, row_heights=[0.7, 0.3])
        
        add_line(fig, col=1, row=1, data=self.portfolio_data, feature="cum_rets", name="cum_rets")
        add_line(fig, col=1, row=1, data=self.portfolio_data, feature="cummax", name="cummax")
        
        add_area(fig, col=1, row=2, data=self.portfolio_data, feature="drawdown", name="drawdown", color = "red")
        fig.update_layout(height = 300 , width = 1200,
                          barmode='stack',
                          legend = dict(orientation="h",
                                        yanchor="bottom", y=1,
                                        xanchor="right", x=0.5),
                          margin = {'t':0, 'b':0, 'l':10, 'r':0}
                          )
        return fig
        
    
    
        