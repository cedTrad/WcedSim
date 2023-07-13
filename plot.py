import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

import numpy as np
import pandas as pd

def line(x, y, color, name):
    fig = go.Scatter(
        x = x, y = y,
        name = name,
        line = dict(color = color, width = 1),
        yaxis='y1'
    )
    return fig


def mark(x, y, color, name):
    fig = go.Scatter(
        x = x, y = y,
        name = name,
         mode = "markers",
        line = dict(color = color, width = 1),
        yaxis='y1'
    )
    return fig
    
    
def candle(data, name):
    fig = go.Candlestick(
            x = data.index , open = data.open, close = data.close,
            high = data.high, low = data.low,
            yaxis='y1'
        )
    return fig


def second_y(x, y, name, color):
    fig = go.Scatter(
        x = x, y = y,
        name = name,
        line = dict(color = color, width = 1),
        yaxis='y2'
    )
    return fig






#  -----------------------------------------------------------------------

# make subplot
def subplots(nb_rows , nb_cols, row_heights = None, column_widths = None, vertical_spacing=0.01, horizontal_spacing = 0.02):
    fig = make_subplots(rows = nb_rows, cols = nb_cols, shared_xaxes = True, shared_yaxes = False,
                        row_heights = row_heights, column_widths= column_widths,
                        vertical_spacing = vertical_spacing, horizontal_spacing = horizontal_spacing,
                         specs = [
                             [{"secondary_y": True}],
                             [{"secondary_y": True}],
                             [{"secondary_y": True}]
                           ]
                         )
    return fig

def subplots2(nb_rows , nb_cols, row_heights = None, column_widths = None, vertical_spacing=0.01, horizontal_spacing = 0.02):
    fig = make_subplots(rows = nb_rows, cols = nb_cols, shared_xaxes = True, shared_yaxes = False,
                        row_heights = row_heights, column_widths= column_widths,
                        vertical_spacing = vertical_spacing, horizontal_spacing = horizontal_spacing
                         )
    return fig


# Plot candle
def plot_candle(fig, col, row, data, symbol):
    fig.add_trace(
        go.Candlestick(
            x = data.index , open = data.open, close = data.close,
            high = data.high, low = data.low, name = symbol,
        ),
        col = col, row = row
    )
    fig = fig.update_xaxes(rangeslider_visible=False)


def add_line(fig, col, row, data, feature, name, color = None):
    fig.add_trace(
        go.Scatter(
            x = data.index,
            y = data[feature],
            name = name
        ),
        col = col, row = row
    )

def add_scatter(fig, col, row, data, name, color):
    fig.add_trace(
        go.Scatter(
            x = data.index,
            y = data[name],
            mode = 'markers',
            marker_color = color,
            name = name
        ),
        col = col, row = row
    )

def add_bar(fig, col, row, data, name):
    fig.add_trace(
        go.Bar(
            x = data.index, y = data[name],
            name = name
        )
    )

def add_hline(fig, y, col, row, color):
    fig.add_hline(y = y , col = col, row = row, line_color = color)


def add_second_y(fig, col, row, data, name = 'position'):
    fig.add_trace(
        go.Scatter(
            x = data.index,
            y = data[name],
            yaxis="y2",
            name = name
        ),
        col = col, row = row,
        secondary_y=True,
    )


# signal point
def signal_point(fig, col, row, x, y, name, marker, size = 10):
    fig.add_trace(
        go.Scatter(
            x = x,
            y = y,
            mode = "markers",
            marker_symbol = marker[0],
            marker_size = marker[1],
            marker_color = marker[2],
            name = name
        ),
        col = col , row = row
    )










def color_trades(fig, col, row, entry, exit, opacity):
    
    entry_date = entry.index.to_list()
    exit_date = exit.index.to_list()
    colors = np.where(entry.type_ == "LONG", 'green', 'red')
    entry_price = entry.price.to_list()
    exit_price = exit.price.to_list()
    
    try:
        for date0, date1, price0, price1, color in zip(entry_date, exit_date, entry_price, exit_price, colors):
            fig.add_shape(x0 = date0, x1 = date1, y0 = price0*0.5, y1 = price1*1.3,
                        fillcolor = color, opacity = opacity,
                        col = col , row = row)
    except:
        ""


def color_returns(fig, col, row, status, x , color, opacity):
    
    fig.add_vrect(x0 = x[0], x1 = x[1],
                  fillcolor = color, opacity = opacity,
                  col = col , row = row)

