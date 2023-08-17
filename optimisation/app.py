import pandas as pd

import datetime
import pytz
from sqlalchemy import create_engine

from app.report import Report
from app.simulation import Simulation

import warnings
warnings.filterwarnings('ignore')



class MApp(Simulation):
    
    def __init__(self, symbols, capital, interval = "1d", start="2023", end="2023", db_trades = "simulation_"):
        Simulation.__init__(self, symbols = symbols, capital = capital,
                     interval = interval, start = start, end = end, db_trades = db_trades)
    
    def run(self):
        self.portfolio.config(m = 3, floor = 0)
        self.set_assets()
        
        bar = 1
        bar_p = 0
        
        placeholder = st.empty()
        progress_bar = st.progress(0)
        st.write(" --- ---- ---")
        while True:
            
            self.apply(bar)
            bar += 1
            with placeholder.container():
                bar_p = (self.n - bar)/self.n
                progress_bar.progress(bar_p)
                
                data = self.journal.data
                portfolio_data = self.journal.portfolio_data
                
                self.report.run(data, portfolio_data)
                
                st.write(f"{bar} / {self.n}")
            if bar == self.n:
                break


def run_simulation(params):
        app = MApp(**params)
        app.run()


portfolios = [
            {"symbols": ["ETH"], "capital": 100, "start": "2023-01", "end": "2023-04", "interval": "1d", "db_trades": "P1"},
            {"symbols": ["XMR"], "capital": 100, "start": "2023-01", "end": "2023-04", "interval": "1d", "db_trades": "P2"},
            {"symbols": ["BTC"], "capital": 100, "start": "2023-01", "end": "2023-04", "interval": "1d", "db_trades": "P3"},
            {"symbols": ["GALA"], "capital": 100, "start": "2023-01", "end": "2023-04", "interval": "1d", "db_trades": "P4"},
            {"symbols": ["EGLD"], "capital": 100, "start": "2023-01", "end": "2023-04", "interval": "1d", "db_trades": "P5"}
        ]


processes = []
for params in portfolios:
    p = multiprocessing.Process(target=run_simulation, args=(params,))
    processes.append(p)
    p.start()
                
for p in processes:
    p.join()
        


