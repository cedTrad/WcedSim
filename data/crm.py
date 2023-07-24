import pandas as pd
import numpy as np

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


from .table import Trades

class DCRM:
    
    def __init__(self):
        self.data = pd.DataFrame()
        self.engine = create_engine(f"sqlite:///data/data.db")
    
    
    
    def add_data(self, add):
        data = Trades(add)
        
        Base.metadata.create_all(self.engine)
        Session = sessionmaker(bind = self.engine)
        session = Session()
                
        session.add(data)
        session.commit()
        session.close()