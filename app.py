from IPython.display import clear_output

from portfolio import Portfolio, Asset
from order import OrderManagement
from signals import Signal
from journal import Journal

from report import Report
from manager import Manager, error_msg

from risk.risk_management import RiskManagement
from db.data import connect_db


class App:
    
    def __init__(self, symbols, capital, interval = "1d", start = "2023", end = "2023"):
        self.symbols = symbols
        self.interval = interval
        self.start = start
        self.end = end
        self.capital = capital
        self.prev_decision = None
        self.order = OrderManagement(capital)
        
        self.portfolio = Portfolio("W", capital)
        
        self.journal = Journal()
        
        self.signal = Signal()
        self.report = Report(start = start, end = end)
        self.manager = Manager(self.portfolio)
        
        
    
    
    def get_signal(self, bar, symbol, interval = "1d"):
        signals = {}
        db = connect_db(name = "database", interval = interval)
        data = db.get_data(symbol, start = self.start, end = self.end)
        self.n = data.shape[0]
        
        data = data.iloc[0:bar].copy()
        self.signal.update_df(data, symbol)
        
        i = -1
        #side = self.signal.get_signal(i)
        model = f"model_{symbol}"
        side = self.signal.get_ml_signal(bar = i , model = model)
        
        date, price = data.index[i], data.close.iloc[i]
        signals = (date, price, side)
        
        return signals
    
    
    def risk_config(self, m, floor):
        self.portfolio.risk.config_cppi(m=m, floor=floor)
          
        
        
    def execute(self, asset, bar):
        symbol = asset.symbol
        signal = self.get_signal(bar, symbol)
        
        decision = signal[2]
        price = signal[1]
        date = signal[0]
        
        self.portfolio.management()
        value_to_risk_p = self.portfolio.risk.value_to_risk
        
        leverage = 1
        
        amount = value_to_risk_p
        quantity = amount / signal[1]
        
        check = self.manager.check_balance(amount)
        
        # Execute
        order = self.order.execute(asset, quantity, signal, check)
        asset = order['asset']
        asset.leverage = leverage
        
        if order['status'] == "LONG" or order['status'] == "SHORT":
            self.portfolio.set_type(asset)
            self.portfolio.rebalance(amount = amount)
        elif order['status'] == '-':
            self.portfolio.update_value(asset)
        elif order["status"] == "C_LONG" or order["status"] == "C_SHORT":            
            self.portfolio.update_value(asset, close=True)
        
        self.journal.save_data(date, price, asset, self.portfolio)
    
    
    def set_assets(self):
        self.assets = {}
        for symbol in self.symbols:
            self.assets[symbol] = Asset(symbol=symbol)
            self.portfolio.add_asset(self.assets[symbol])
    
    
    def apply(self, bar):
        for symbol in self.symbols:
            self.execute(self.assets[symbol], bar)
        
    
    def run(self):
        
        self.portfolio.config(m = 3, floor = 0)
        self.set_assets()
        bar = 1
        
        while True:
            self.apply(bar)
            
            bar += 1
            clear_output(wait = True)
            
            data = self.journal.data
            portfolio_data = self.journal.portfolio_data
            
            #self.report.run(data, portfolio_data)
            
            self.report.run()
            display(data)
            
            if bar == self.n:
                break
        