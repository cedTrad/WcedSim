import pandas as pd
import numpy as np
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import uuid

from .db.base import Base, Base_metrics
from .db.table import Trades, Portfolio_tab, Metrics


class Journal:
    
    def __init__(self, db_trades):
        self.name = 'w'
        self.portfolio_data = pd.DataFrame()
        self.metrics_data = pd.DataFrame()
        self.data = pd.DataFrame()
        self.engine = create_engine(f"sqlite:///data/{db_trades}.db")
    
    def set_date(self, date):
        self.date = date
        
    def asset(self, date, price, asset):
        data = {'date' : date, 'price' : price, 
                'quantity' : asset.quantity, 'position' : asset.position,
                'side' : asset.type, 'status' : asset.status,
                'in_value' : asset.in_value,
                'out_value' : asset.out_value,
                'value' : asset.value, 'pnl' : asset.pnl, 'pnl_pct' : asset.pnl_pct,
                'symbol' : asset.symbol}
        add = pd.DataFrame(data , index = [date])
        self.data = pd.concat([self.data, add], ignore_index = True)
        #self.data = self.data.append(add)
        
        data['key'] = str(uuid.uuid1())
        data = Trades(data)
        self.to_database(data, self.engine)
    
        
    def portfolio(self, date, portfolio):
        data = {'date' : date, 'risk_value' : portfolio.risk_value,
                'available_value' : portfolio.available_value, 'capital' : portfolio.capital,
                'value_to_risk' : portfolio.risk.value_to_risk,
                'value_to_safe' : portfolio.risk.value_to_safe,
                'floor_value' : portfolio.risk.floor_value ,'cushion' : portfolio.risk.cushion,
                'risky_w' : portfolio.risk.risky_w}
        
        add = pd.DataFrame(data, index = [date])
        self.portfolio_data = pd.concat([self.portfolio_data, add], ignore_index = True)
        
        data['key'] = str(uuid.uuid1())
        data = Portfolio_tab(data)
        self.to_database(data, self.engine)
    
    
    def save_metrics(self, data):
        add = pd.DataFrame(data, index = ["0"])
        self.metrics_data = pd.concat([self.metrics_data, add], ignore_index = True)
        
        data['key'] = str(uuid.uuid1())
        data = Metrics(data)
        self.to_database(data, self.engine)
        
        
    def save_data(self, date, price, asset, portfolio):
        self.asset(date, price, asset)
        self.portfolio(date, portfolio)
        
        
    def to_database(self, data, engine):
        Base.metadata.create_all(engine)
        Session = sessionmaker(bind = engine)
        session = Session()
        
        session.add(data)
        session.commit()
        session.close()


