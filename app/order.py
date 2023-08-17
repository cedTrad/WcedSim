
class OrderManagement:
    
    def __init__(self, capital):
        self.capital = capital
    
    
    def place_order(self, symbol, price, quantity, side):
        quantity = abs(quantity)
        order = {
            'symbol' : symbol,
            'quantity' : quantity,
            'side' : side
        }
        if side == "BUY":
            return quantity
        elif side == "SELL":
            return (-1)*quantity
    
    
    def open_long(self, asset, price, quantity):
        qty = self.place_order(asset.symbol, price, quantity, side = "BUY")
        asset.type = "LONG"
        asset.position = 1
        asset.update(quantity = qty, price = price, status = "open")
        return {'asset' : asset, 'status' : 'LONG'}
    
    
    def close_long(self, asset, price):
        qty = self.place_order(asset.symbol, price, quantity = asset.quantity, side = "SELL")
        asset.position = 0
        asset.update(quantity = qty, price = price, status = "close")
        asset.type = "None"
        return {'asset' : asset, 'status' : 'C_LONG'}
        
        
    def open_short(self, asset, price, quantity):
        qty = self.place_order(asset.symbol, price, quantity, side = "SELL")
        asset.type = "SHORT"
        asset.position = -1
        asset.update(quantity = qty, price = price, status = "open")
        return {'asset' : asset, 'status' : 'SHORT'}
    
    
    def close_short(self, asset, price):
        qty = self.place_order(asset.symbol, price, quantity = asset.quantity, side = "BUY")
        asset.position = 0
        asset.update(quantity = qty, price = price, status = "close")
        asset.type = "None"
        return {'asset' : asset, 'status' : 'C_SHORT'}
        
    
    def execute(self, asset, quantity, signal, check):
        date, price, decision = signal
        symbol = asset.symbol
        position = asset.position
        
        #if check == 100:
            #print("ok for order")
        
        if position == 0 and decision == "LONG" and check == 100:
            order = self.open_long(asset, price, quantity)
        
        elif position == -1 and decision == "LONG":
            order = self.close_short(asset, price)
            
        elif position == 0 and decision == "SHORT" and check == 100:
            order = self.open_short(asset, price, quantity)
        
        elif position == 1 and decision == "SHORT":
            order = self.close_long(asset, price)
        
        elif position == 1 and decision == "None":
            order = self.close_long(asset, price)
        
        elif position == -1 and decision == "None":
            order = self.close_short(asset, price)
            
        #elif position == 0 and decision == "None":
            #order = {'asset' : asset, 'status' : "-"}
        
        else:
            asset.update(price = price)
            order = {'asset' : asset, 'status' : "-"}
            
        return order
    
        
