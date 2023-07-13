import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

import streamlit as st 
from streamlit_option_menu import option_menu

from sqlalchemy import create_engine

from report import Report
from app import App
from utils import assets

import warnings
warnings.filterwarnings('ignore')


class StApp(App):
    
    def __init__(self, symbol, capital):
        App.__init__(self, symbol, capital)
        
    def run(self, report):
        self.set_assets()
        self.report = report()
        
        bar = 0
        bar_p = 0
        stop = 160
        
        placeholder = st.empty()
        progress_bar = st.progress(0)
        while True:
            
            self.apply(bar)
            
            bar += 1
            bar_p = (stop - bar)/stop
            progress_bar.progress(bar_p)
            
            self.report.run()
            
            data = self.journal.data
            portfolio_data = self.journal.portfolio_data
            
            with placeholder.container():
                col1, col2 = st.columns(2)
                with col1:
                    fig = px.line(portfolio_data[['risk_value', 'safe_value', 'capital']])
                    st.plotly_chart(fig)
                with col2:
                    fig = self.report.plot("pnl")
                    st.plotly_chart(fig, True)
            
            if bar == stop:
                break
            
            





SYMBOLS = ['BTC', 'ETH', 'DASH']

st.set_page_config(page_title="Trading System",
                    page_icon=":female-doctor",
                    layout="wide")
        
st.title("Backtesting")

side = st.sidebar


selected = option_menu(
                    menu_title=None, 
                    options=["View", "Run"],
                    icons=["pencil-fill", "bar-chart-fill"],
                    orientation="horizontal"
                    )

if selected == "Run":
    with st.form("config"):
        col1, col2 = st.columns(2)
        with col1:
            symbols = st.multiselect("choose cryptocurrency ", tuple(assets), key="symbols")
        with col2:
            capital = st.number_input("capital", key="capital")
            
        run_button = st.form_submit_button("Run")
        if run_button:
            app = StApp(symbols, capital)
            app.run(Report)
            
                

if selected == "View":
    report = Report()
    report.run()
    col1, col2 = st.columns([1, 3])
    with col1:
        st.write(report.metrics.df)
    
    with col2:
        fig = report.plot("pnl")
        st.plotly_chart(fig, True)
        
    
    symbol = st.selectbox("choose cryptocurrency ", tuple(report.symbols), key="symbol")
    fig = report.plot_asset(symbol)
    st.plotly_chart(fig, True)
    
    fig = report.plot_portfolio()
    st.plotly_chart(fig)
    st.write(" - - - ")

#streamlit run c:/Users/cc/Desktop/W/dash.py



