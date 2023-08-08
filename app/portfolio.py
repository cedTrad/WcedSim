import numpy as np
import pandas as pd

from .risk.risk_management import RiskManagement

from utils import assets


class Asset:
    
    def __init__(self, symbol):
        self.symbol = symbol
        self.quantity = 0
        self.value = 0
        self.leverage = 1
        self.borrow = 0
        self.position = 0
        self.in_value = 0
        self.out_value = 0
        self.pnl = 0
        self.pnl_pct = 0
        self.type = ""
        self.status = ""
        
    
    def set_leverage(self, leverage):
        self.leverage = leverage
    
    
    def pnl_value(self, price):
        self.pnl = (self.quantity * price - self.in_value)
        if self.type == "SHORT":
            self.pnl = (self.in_value - abs(self.quantity) * price)
            if self.quantity == 0:
                self.pnl = -self.in_value
    
    
    def get_value(self, price):
        self.pnl_value(price)
        value = self.in_value + self.pnl * self.leverage
        return value
        
        
    def update(self, price, quantity = 0, status = "-"):   
        if status == "open":
            self.quantity += quantity
            self.in_value = abs(self.quantity * price)
            self.value = self.get_value(price)
            self.pnl_pct = (self.pnl / self.in_value)
            self.status = status
            self.out_value = 0
        
        elif status == "close":
            self.out_value = abs(self.quantity * price)
            self.quantity += quantity
            self.value = self.get_value(price)
            self.pnl = self.out_value - self.in_value
            self.pnl_pct = (self.pnl / self.in_value)
            self.status = status
            self.in_value = 0
        
        else:
            self.status = status
            self.value = self.get_value(price)
            self.out_value = 0
            try:
                self.pnl_pct = (self.pnl / self.in_value)
            except:
                self.pnl_pct = 0





class Portfolio:
    
    def __init__(self, name, capital):
        self.name = name
        self.capital = capital
        self.init_capital = capital
        
        self.assets = {}
        self.assets_long = {}
        self.assets_short = {}
        
        self.risk_value = 0
        self.available_value = capital
        
        self.positions = {}
        self.long_value = 0
        self.short_value = 0
        
        self.type = ""
        
        self.risk = RiskManagement(capital)
        
        
    def add_asset(self, asset, w = 1):
        self.assets[asset.symbol] = {'asset' : asset, 'weigth' : w}
        
        
    def remove_asset(self, asset):
        del self.assets[asset.symbol]
    
    
    def update_assets(self, asset, w = 1):
        self.assets[asset.symbol] = {'asset' : asset, 'weigth' : w}
        
            
    def update_risky(self, asset, close = False):
        values = 0
        self.update_assets(asset)
        for asset in self.assets.values():
            values += asset['asset'].value
        self.risk_value = values
        
    
    def update_value(self, asset, close = False): # rebalance
        self.update_risky(asset)
        
        if close:
            amount = asset.out_value
            self.available_value += amount
            
        self.capital = self.risk_value + self.available_value
        
    
    def rebalance(self, amount):        
        self.risk_value += amount
        self.available_value -= amount
        self.capital = self.risk_value + self.available_value
        
    
    
    def set_type(self, asset):
        symbol = asset.symbol
        if asset.type == "SHORT":
            self.assets_short[symbol] = asset
        elif asset.type == "LONG":
            self.assets_long[symbol] = asset
    
    
    def config(self, m, floor):
        self.risk.config_cppi(m=m, floor=floor)
    
    
    def management(self):
        self.risk.run(self.capital)
        


