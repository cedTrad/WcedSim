from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, Integer, Date, Float, Boolean, ForeignKey

from .base import Base


class Trades(Base):
    __tablename__ = "trades"
    time = Column(String, primary_key = True)
    price = Column(Float)
    quantity = Column(Float)
    position = Column(Float)
    type_ = Column(String)
    status = Column(String)
    in_value = Column(Float)
    out_value = Column(Float)
    value = Column(Float)
    pnl = Column(Float)
    symbol = Column(String)
    
    def __init__(self, add):
        self.date = str(add['date'])
        self.price = add['price']
        self.quantity = add['quantity']
        self.position = add['position']
        self.type_ = add['type']
        self.status = add['status']
        self.in_value = add['in_value']
        self.out_value = add['out_value']
        self.value = add['value']
        self.pnl = add['pnl']
        self.symbol = add['symbol']
        
        