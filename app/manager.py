import pandas as pd
import numpy as np 


error_msg = {
    100 : 'no_probleme , order can be placed',
    101 : 'no_enought_amount',
    102 : 'no_enought_amount , thresold'
}

class Manager:
    
    def __init__(self, portfolio):
        self.portfolio = portfolio
        self.thresold_amount = 11
        
    def check_balance(self, amount):
        if self.portfolio.available_value < amount:
            return 101
        elif amount < self.thresold_amount:
            return 102
        else:
            return 100        # ok 
    
    def stop(self):
        if self.portfolio.capital < 10:
            return stop
        
    
        