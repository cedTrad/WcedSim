import pandas as pd
import numpy as np

import scipy.stats
from scipy.stats import norm


pd.options.display.float_format = '{:.2f}'.format
    
class Metric:
    
    def __init__(self, assets_data):
        self.assets_data = assets_data
        self.n_trades = 0
        self.symbols = list(assets_data.keys())
        self.df = pd.DataFrame(index = ["total_pnl", "expentancy", "win_rate", "loss_rate",
                                        "amoung_win", "amoung_loss", "avg_win", "avg_loss",
                                        "profit_factor"]
                               )
        self.portfolio_df = pd.DataFrame(index = ["total_pnl", "expentancy", "amoung_win", "amoung_loss",
                                                  "avg_win", "avg_loss", "profit_factor"])
        self.df_st = pd.DataFrame()
        self.add_st = {}
    
    
    def get_stats(self, symbol):
        add_st = {}
        add_st["date"] = self.date
        add_st["symbol"] = symbol
        add_st["n_trades"] = self.n_trades
        add_st["total_pnl"] = self.total_pnl
        add_st["expentancy"] = self.exp
        add_st["win_rate"] = self.win_rate
        add_st["loss_rate"] = self.loss_rate
        add_st["amoung_win"] = self.amoung_win
        add_st["amoung_loss"] = self.amoung_loss
        add_st["avg_gp"] = self.avg_gp
        add_st["avg_win"] = self.avg_win
        add_st["avg_loss"] = self.avg_loss
        add_st["profit_factor"] = self.profit_factor
        return add_st
    
    
    
    def pnl(self, r):
        x = (1 + r).prod()
        return x    

    
    def average(self, r):
        if len(r) == 0:
            return 0
        else:
            x = (1+r).prod()
            return x**(1/len(r))
    
    
    def expectancy(self, win_rate, avg_win, avg_loss):
        return win_rate*avg_win + (1 - win_rate)*avg_loss    
    
    def sharpe_ratio(self):
        return
    
    def positions(self, r):
        pos = {"min" : 0, "25%" : 0, "median" : 0, "75%" : 0, "max" : 0}
        if len(r)>8:
            pos["min"] = r.min()
            pos["25%"] = np.percentile(r, 0.25)
            pos["50%"] = np.percentile(r, 0.5)
            pos["avg"] = self.average(r)
            pos["75%"] = np.percentile(r, 0.75)
            pos["max"] = r.max()
        return pos
    
    
    def kurtosis(self, r, n = 8):
        if len(r) > n:
            return scipy.stats.kurtosis(r)
        else:
            return 0

    def skewness(self, r, n = 8):
        if len(r) > n:
            return scipy.stats.skew(r)
        else:
            return 0
    
    
    def stats(self, data):
        try:
            self.date = str(data.index[-1])
        except IndexError:
            self.date = None
        loc = np.where((data.status == "close"))
        self.n_trades = len(loc[0])
        loc = np.where((data.status == "close") & (data.pnl > 0))
        self.win_trades = len(loc[0])
        loc = np.where((data.status == "close") & (data.pnl <= 0))
        self.loss_trades = len(loc[0])
        
        try:
            self.win_rate = self.win_trades / self.n_trades
        except ZeroDivisionError:
            self.win_rate = 0
        try:
            self.loss_rate = self.loss_trades / self.n_trades
        except ZeroDivisionError:
            self.loss_rate = 0
        
        loc = np.where(data.gp != 0)
        self.avg_gp = data.iloc[loc]["gp"].mean()
        self.amoung_win = data.loc[data.gp > 0, "gp"].sum()
        self.amoung_loss = data.loc[data.gp <= 0, "gp"].sum()
        
        data_ = data.iloc[loc]
        self.avg_win = data_.loc[data_.gp > 0, "gp" ].mean()
        self.avg_loss = data_.loc[data_.gp <= 0, "gp" ].mean()
        self.profit_factor = self.amoung_win / abs(self.amoung_loss)
        
        
        
    def kpi(self, symbol, data):
        self.stats(data)
        
        self.total_pnl = data.gp.sum()
        self.exp = self.expectancy(win_rate = self.win_rate,
                                   avg_win = self.avg_win,
                                   avg_loss = self.avg_loss)
        col = [self.total_pnl, self.exp, self.win_rate, self.loss_rate,
               self.amoung_win, self.amoung_loss, self.avg_win, self.avg_loss,
               self.profit_factor]
        self.df[symbol] = col
        add = self.get_stats(symbol)
        return add
        
        
    def run(self):
        dd = {}
        for symbol in self.symbols:
            temp = {}
            data = self.assets_data[symbol]["data"].copy()
            data_long = self.assets_data[symbol]["long"].copy()
            data_short = self.assets_data[symbol]["short"].copy()
            
            temp["data"] = self.kpi(symbol, data)
            temp["long"] = self.kpi(symbol, data_long)
            temp["short"] = self.kpi(symbol, data_short)
            
            dd[symbol] = temp
            
        return dd