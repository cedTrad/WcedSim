import pandas as pd
import json

import plotly.graph_objects as go
from .plot import add_line

from .evaluation.metric import Metric
from .preprocessing import Preprocessing
from app.journal import Journal



class PNL(Metric):
    
    def __init__(self, db_trades):
        self.journal = Journal(db_trades = db_trades)
        self.preprocessing = Preprocessing()
    
    
    def get_trades(self, assets_data):
        self.assets_data = assets_data
        self.metrics = Metric(assets_data = assets_data)
        self.symbols = list(assets_data.keys())
    
    
    def run(self):
        data = self.metrics.run()
        for symbol in self.symbols:
            self.journal.save_metrics(data[symbol]["data"])
    
    
    def report(self, engine):
        data = pd.read_sql('metrics', engine)
        self.metrics_data = self.preprocessing.split_metrics(data)
        
    
    def viz_distribution(self, symbol):
        data_long = self.assets_data[symbol]["long"]
        data_short = self.assets_data[symbol]["short"]
        
        fig = go.Figure()
        fig.add_trace(
            go.Histogram(x = data_long.gp, marker_color='blue',
                         name = "long")
        )
        fig.add_trace(
            go.Histogram(x = data_short.gp, marker_color = 'red',
                         name = "short")
        )
        fig.update_layout(height = 300 , width = 800,
                          margin = {'t':0, 'b':0, 'l':0}
                          )
        return fig
    
    
    def plot_metric(self, symbol, features):
        data = self.metrics_data[symbol]
        
        fig = go.Figure()
        if isinstance(features, list):
            for feature in features:
                add_line(fig = fig, data = data, feature = feature, name = feature)
        else:
            add_line(fig = fig, data = data, feature = feature, name = feature)
        fig.update_layout(height = 500 , width = 1000,
                          margin = {'t':0, 'b':0, 'l':0}
                          )
        return fig
    
    
        



