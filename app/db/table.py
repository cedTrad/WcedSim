from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, Integer, Date, Float, Boolean, ForeignKey

from .base import Base


class Trades(Base):
    __tablename__ = "trades"
    #__abstract__ = True
    key = Column(String, primary_key = True)
    date = Column(String)
    price = Column(Float)
    quantity = Column(Float)
    position = Column(Float)
    side = Column(String)
    status = Column(String)
    in_value = Column(Float)
    out_value = Column(Float)
    value = Column(Float)
    pnl = Column(Float)
    pnl_pct = Column(Float)
    symbol = Column(String)
    
    def __init__(self, add):
        self.key = add['key']
        self.date = str(add['date'])
        self.price = add['price']
        self.quantity = add['quantity']
        self.position = add['position']
        self.side = add['side']
        self.status = add['status']
        self.in_value = add['in_value']
        self.out_value = add['out_value']
        self.value = add['value']
        self.pnl = add['pnl']
        self.pnl_pct = add['pnl_pct']
        self.symbol = add['symbol']
        
        

class Portfolio_tab(Base):
    __tablename__ = "portfolio_tab"
    key = Column(String, primary_key = True)
    date = Column(String)
    risk_value = Column(Float)
    available_value = Column(Float)
    capital = Column(Float)
    
    value_to_risk = Column(Float)
    value_to_safe = Column(Float)
    
    floor_value = Column(Float)
    cushion = Column(Float)
    m = Column(Integer)
    risky_w = Column(Float)
    
    margin = Column(Integer)
    risk_value = Column(Float)
    
    
    
    def __init__(self, add):
        self.key = add['key']
        self.date = str(add['date'])
        self.risk_value = add['risk_value']
        self.available_value = add['available_value']
        self.capital = add['capital']
        self.value_to_risk = add['value_to_risk']
        self.value_to_safe = add['value_to_safe']
        self.floor_value = add['floor_value']
        self.cushion = add['cushion']
        self.risky_w = add['risky_w']
        



class Metrics(Base):
    __tablename__ = "metrics"
    key = Column(String, primary_key = True)
    date = Column(String)
    symbol = Column(String)
    total_pnl = Column(Float)
    expentancy = Column(Float)
    win_rate  = Column(Float)
    loss_rate = Column(Float)
    amoung_win  = Column(Float)
    amoung_loss = Column(Float)
    avg_gp = Column(Float)
    avg_win = Column(Float)
    avg_loss = Column(Float)
    profit_factor = Column(Float)
    
    def __init__(self, add):
        self.key = add["key"]
        self.date = add["date"]
        self.symbol = add["symbol"]
        self.total_pnl = add["total_pnl"]
        self.expentancy = add["expentancy"]
        self.win_rate = add["win_rate"]
        self.loss_rate = add["loss_rate"]
        self.amoung_win = add["amoung_win"]
        self.amoung_loss = add["amoung_loss"]
        self.avg_gp = add["avg_gp"]
        self.avg_win = add["avg_win"]
        self.avg_loss = add["avg_loss"]
        self.profit_factor = add["profit_factor"]


