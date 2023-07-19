import pandas as pd
import numpy as np
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import uuid

from db.base import Base
from db.table import Trades, Portfolio_tab


class Journal:
    
    def __init__(self, name = 'w'):
        self.name = 'w'
        self.portfolio_data = pd.DataFrame()
        self.data = pd.DataFrame()
        self.engine = create_engine(f"sqlite:///db/data_.db")
        
        
    def asset(self, date, price, asset):
        data = {'date' : date, 'price' : price, 
                'quantity' : asset.quantity, 'position' : asset.position,
                'type' : asset.type, 'status' : asset.status,
                'in_value' : asset.in_value,
                'out_value' : asset.out_value,
                'value' : asset.value, 'pnl' : asset.pnl, 'pnl_pct' : asset.pnl_pct,
                'symbol' : asset.symbol}
        add = pd.DataFrame(data , index = [date])
        self.data = self.data.append(add)
        
        data['key'] = str(uuid.uuid1())
        data = Trades(data)
        self.to_database(data)
    
        
    def portfolio(self, date, portfolio):
        data = {'date' : date, 'risk_value' : portfolio.risk_value,
                'safe_value' : portfolio.safe_value, 'capital' : portfolio.capital}
        add = pd.DataFrame(data, index = [date])
        self.portfolio_data = self.portfolio_data.append(add)
        
        data['key'] = str(uuid.uuid1())
        data = Portfolio_tab(data)
        self.to_database(data)
        
        
        
    def save_data(self, date, price, asset, portfolio):
        self.asset(date, price, asset)
        self.portfolio(date, portfolio)
        
        
    def to_database(self, data):
        Base.metadata.create_all(self.engine)
        Session = sessionmaker(bind = self.engine)
        session = Session()
        
        session.add(data)
        session.commit()
        session.close()