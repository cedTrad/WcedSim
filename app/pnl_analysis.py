import pandas as pd
import json

import plotly.graph_objects as go
from .plot import add_line

from .evaluation.metric import Metric
from .preprocessing import Preprocessing


class PNL(Metric):
    
    def __init__(self, journal = None):
        self.journal = journal
        self.preprocessing = Preprocessing()
    
    
    def get_trades(self, assets_data):
        self.assets_data = assets_data
        self.metrics = Metric(assets_data = assets_data)
        self.symbols = list(assets_data.keys())
    
    
    def run(self, monitoring = True):
        data = self.metrics.run()
        for symbol in self.symbols:
            self.journal.metrics(data[symbol]["data"], monitoring)
            #self.journal.metrics(data[symbol]["long"])
            #self.journal.metrics(data[symbol]["short"])
        m_data = self.journal.metrics_data
        self.metrics_data = self.preprocessing.split_metrics(m_data)
            
    
    #def report(self, engine):
    #    data = pd.read_sql('metrics', engine)
    #    self.metrics_data = self.preprocessing.split_metrics(data)
        
    
    def viz_distribution(self, symbol, assets_data = None):
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
    
    
    def plot_metric(self, symbol, features, metrics_data = None):
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
    
    
        



