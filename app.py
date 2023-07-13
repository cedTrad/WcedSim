from IPython.display import clear_output

from portfolio import Portfolio, Asset
from data import connect_db
from order import OrderManagement
from signals import Signal
from journal import Journal

from manager import Manager, error_msg

from risk.cppi import CPPI

#from base import update_data

class App:
    
    def __init__(self, symbols, capital):
        self.symbols = symbols
        
        self.capital = capital
        self.prev_decision = None
        self.order = OrderManagement(capital)
        self.portfolio = Portfolio("W", capital)
        self.journal = Journal()
        self.cppi = CPPI(capital)
        
        self.manager = Manager(self.portfolio)
        
    
    def updateData(self, interval):
        update_data(self.symbols, interval)
    
    
    def get_signal(self, bar):
        signals = {}
        db = connect_db(name = "database_1d.db")
        start = '2023'
        
        for symbol in self.symbols:
            data = db.get_data(symbol, start = start)
            
            signal = Signal(data)
            side = signal.get_signal(bar)
            #model = f"model_{symbol}"
            #side = signal.get_ml_signal(bar, model = model)
            
            date, price = data.index[bar], data.close.iloc[bar]
            signals[symbol] = (date, price, side)
        return signals
        
        
    def execute(self, asset, bar):
        symbol = asset.symbol
        signal = self.get_signal(bar)[symbol]
        
        decision = signal[2]
        price = signal[1]
        date = signal[0]
        
        #amount = self.portfolio.safe_value * 0.9
        amount = self.portfolio.safe_value * 0.3
        #amount = self.portfolio.capital
        quantity = amount / signal[1]
        
        check = self.manager.check_balance(amount)
        
        # Execute
        order = self.order.execute(asset, quantity, signal, check)
        asset = order['asset']
        
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
        
    
    def run(self, report):
        
        self.set_assets()
        self.report = report()
        bar = 0
        while True:
            
            self.apply(bar)
            
            bar += 1
            clear_output(wait = True)
            
            data = self.journal.data
            portfolio_data = self.journal.portfolio_data
            
            #self.report.run(data, portfolio_data)
            self.report.run()
            display(data)
            
            if bar == 120:
                break
        