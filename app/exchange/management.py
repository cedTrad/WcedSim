

from account import Account

class Management:
    
    def __init__(self):
        self.account = Account()
        
    def futureAccountInfo(self):
        account = self.account.info()
        
        tems1 = ['initialMargin', 'maintMargin', 'unrealizedProfit', 'positionInitialMargin', 
                  'openOrderInitialMargin', 'positionAmt', 'entryPrice', 'leverage', 'isolated']
        
        items2 = ['markPrice' ,'notional', 'liquidationPrice', 'updateTime']
        
        self.positions = {}
        for position in account['positions']:
            if position['entryPrice'] != '0.0':
                temp = {key : position[key] for key in items1}
                self.positions[position['symbol']] = temp
        
        for symbol in self.positions.keys():
            for key in items2:
                #temp = {key : self.positionInfo(symbol)[0][key] for key in items2}
                self.positions[symbol][key] = self.account.positionInfo(symbol)[0][key]
        
    
    def get_all_position(self):
        ""
    
    def close_position(self):
        ""