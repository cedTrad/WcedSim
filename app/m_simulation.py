import pandas as pd

import datetime
import pytz
from sqlalchemy import create_engine

from report import Report
from simulation import Simulation

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




def simulation_trading(**params):
    app = MStApp(**params)
    app.run()
    

simulation_params = [
        {"symbols": ["ETH", "BTC"], "capital": 10000, "start": "2023-01-01", "end": "2023-01-31", "interval": "1d", "db_trades": "sim1"},
        {"symbols": ["EGLD", "XMR"], "capital": 15000, "start": "2023-02-01", "end": "2023-02-28", "interval": "1d", "db_trades": "sim2"}
    ]



processes = []
for params in params_list:
    p = multiprocessing.Process(target=create_and_run_app, args=(params,))
    processes.append(p)
    p.start()
for p in processes:
    p.join()

print("All simulations are completed.")
            