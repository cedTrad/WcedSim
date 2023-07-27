import pandas as pd

import plotly.graph_objects as go

from .evaluation.metric import Metric


class PNL(Metric):
    
    def __init__(self, data):
        Metric.__init__(self, data)
        self.data = data
        self.symbols = list(data.keys())
    
    def run(self, symbol):
        self.data_long = self.data[symbol]["long"]
        self.data_short = self.data[symbol]["short"]
        self.kpi("long", self.data_long)
        self.kpi("short", self.data_short)
    
    def viz_distribution(self):
        fig = go.Figure()
        
        fig.add_trace(
            go.Histogram(x = self.data_long.gp)
        )
        fig.add_trace(
            go.Histogram(x = self.data_short.gp)
        )
        
        return fig