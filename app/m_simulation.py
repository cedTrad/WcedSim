import pandas as pd

import datetime
import pytz
from sqlalchemy import create_engine

from app.report import Report
from app.simulation import Simulation
from utils import assets

import warnings
warnings.filterwarnings('ignore')



class MStApp(Simulation):
    
    def __init__(self, symbols, capital, interval = "1d", start="2023", end="2023", db_name = "data"):
        Simulation.__init__(self, symbols = symbols, capital = capital,
                     interval = interval, start = start, end = end, db_name = db_name)
        self.portfolio = []
        
        
    def run(self):
        
        self.portfolio.config(m = 3, floor = 0)
        asset = Asset(symbol=symbol)
        self.portfolio.add_asset(asset)
        bar = 1
        
        while True:
            self.execute(asset, bar)
            
            bar += 1
            clear_output(wait = True)
            
            data = self.journal.data
            portfolio_data = self.journal.portfolio_data
            
            self.report.run(data, portfolio_data)
            
            #self.report.run()
            display(data)
            
            if bar == self.n:
                break
    
            