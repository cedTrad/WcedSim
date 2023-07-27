import pandas as pd
import numpy as np

import scipy.stats
from scipy.stats import norm


pd.options.display.float_format = '{:.2f}'.format
    
class Metric:
    
    def __init__(self, data):
        self.data = data
        self.n_trades = 0
        self.symbols = list(data.keys())
        self.df = pd.DataFrame(index = ["total_pnl", "expentancy", "win_rate", "loss_rate",
                                        "amoung_win", "amoung_loss", "avg_win", "avg_loss"]
                               )
        self.portfolio_df = pd.DataFrame(index = ["total_pnl", "expentancy", "amoung_win", "amoung_loss",
                                                  "avg_win", "avg_loss"])
        self.df_st = pd.DataFrame()
        
        self.add_st = {"total_pnl": 0, "expentancy" : 0, "win_rate" : 0, "loss_rate" : 0,
                    "amoung_win" : 0, "amoung_loss" : 0, "avg_win" : 0, "avg_loss" : 0,
                    "symbol" : ""}
    
    
    def add_stats(self, symbol):
        self.add_st["symbol"] = symbol
        self.add_st["n_trades"] = self.n_trades
        self.add_st["total_pnl"] = self.total_pnl
        self.add_st["expentancy"] = self.expectancy
        self.add_st["win_rate"] = self.win_rate
        self.add_st["loss_rate"] = self.loss_rate
        self.add_st["amoung_win"] = self.amoung_win
        self.add_st["amoung_loss"] = self.amoung_loss
        self.add_st["avg_win"] = self.avg_win
        self.add_st["avg_loss"] = self.avg_loss
    
    
    
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

    
    def profit_factor(self):
        return
    
    
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
        
        
        
    def kpi(self, symbol, data):
        self.stats(data)
        
        self.total_pnl = data.gp.sum()
        self.exp = self.expectancy(win_rate = self.win_rate,
                                   avg_win = self.avg_win,
                                   avg_loss = self.avg_loss)
        
        col = [self.total_pnl, self.exp, self.win_rate, self.loss_rate,
               self.amoung_win, self.amoung_loss, self.avg_win, self.avg_loss]
        self.df[symbol] = col
        self.add_stats(symbol)
        
        
    def run(self):
        for symbol in self.symbols:
            data = self.data[symbol]["data"]
            self.kpi(symbol, data)
            