import pandas as pd
import numpy as np
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import uuid

from .db.base import Base
from .db.table import Trades, Portfolio_tab, Metrics


class Journal:
    
    def __init__(self, db_trades):
        self.name = 'w'
        self.portfolio_data = pd.DataFrame()
        self.metrics_data = pd.DataFrame()
        self.data = pd.DataFrame()
        self.engine = create_engine(f"sqlite:///data/{db_trades}")
    
    
    def set_date(self, date):
        self.date = date
        
        
    def asset(self, date, price, asset, monitoring):
        data = {'date' : date, 'price' : price, 
                'quantity' : asset.quantity, 'position' : asset.position,
                'side' : asset.type, 'status' : asset.status,
                'in_value' : asset.in_value,
                'out_value' : asset.out_value,
                'value' : asset.value, 'pnl' : asset.pnl, 'pnl_pct' : asset.pnl_pct,
                'symbol' : asset.symbol}
        add = pd.DataFrame(data , index = [date])
        self.data = pd.concat([self.data, add], ignore_index = True)
        
        if not monitoring:
            data['key'] = str(uuid.uuid1())
            data = Trades(data)
            self.to_database(data, self.engine)
        
        
    def portfolio(self, date, portfolio, monitoring):
        data = {'date' : date, 'risk_value' : portfolio.risk_value,
                'available_value' : portfolio.available_value, 'capital' : portfolio.capital,
                'value_to_risk' : portfolio.risk.value_to_risk,
                'value_to_safe' : portfolio.risk.value_to_safe,
                'floor_value' : portfolio.risk.floor_value ,'cushion' : portfolio.risk.cushion,
                'risky_w' : portfolio.risk.risky_w}
        
        add = pd.DataFrame(data, index = [date])
        self.portfolio_data = pd.concat([self.portfolio_data, add], ignore_index = True)
        if not monitoring:
            data['key'] = str(uuid.uuid1())
            data = Portfolio_tab(data)
            self.to_database(data, self.engine)
    
    
    def metrics(self, data, monitoring):
        add = pd.DataFrame(data, index = ["0"])
        self.metrics_data = pd.concat([self.metrics_data, add], ignore_index = True)
        if not monitoring:
            data['key'] = str(uuid.uuid1())
            data = Metrics(data)
            self.to_database(data, self.engine)
        
        
    def add_data(self, date, price, asset, portfolio, monitoring = True):
        self.asset(date, price, asset, monitoring)
        self.portfolio(date, portfolio, monitoring)
        
        
    def to_database(self, data, engine):
        Base.metadata.create_all(engine)
        Session = sessionmaker(bind = engine)
        session = Session()
        
        session.add(data)
        session.commit()
        session.close()


    def save_data(self):
        
        self.data.to_sql("trades", self.engine, if_exists='replace')
        self.portfolio_data.to_sql("portfolio_tab", self.engine, if_exists='replace')
        self.metrics_data.to_sql("metrics", self.engine, if_exists='replace')
        
        
        
