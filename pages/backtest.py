import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

import streamlit as st 
from streamlit_option_menu import option_menu

import datetime
import pytz
from sqlalchemy import create_engine

from app.report import Report
from app.simulation import Simulation
from utils import assets

import warnings
warnings.filterwarnings('ignore')



class StApp(Simulation):
    
    def __init__(self, symbols, capital, interval = "1d", start="2023", end="2023"):
        Simulation.__init__(self, symbols = symbols, capital = capital,
                     interval = interval, start = start, end = end)
    
    def run(self):
        
        self.portfolio.config(m = 3.5, floor = 0.7)
        
        self.set_assets()
        
        bar = 1
        bar_p = 0
        
        placeholder = st.empty()
        progress_bar = st.progress(0)
        
        while True:
            self.apply(bar)
            bar += 1
            
            bar_p = (self.n - bar)/self.n
            progress_bar.progress(bar_p)
            
            data = self.journal.data
            portfolio_data = self.journal.portfolio_data
            
            #self.report.run(data, portfolio_data)
            self.report.run()
            
            with placeholder.container():
                col1, col2, col3 = st.columns([3, 1, 1])
                with col1:
                    st.dataframe(data.drop(columns=["date", "position", "out_value"]).iloc[-len(self.symbols):])
                with col2:
                    st.dataframe(portfolio_data.drop(columns=["date"]).iloc[-1])
                with col3:
                    st.write(self.report.metrics.df)
                
                st.title(" ----- ----- ----- -----")
                col1, col2 = st.columns(2)
                with col1:
                    fig = self.report.plot("cum_gp")
                    st.plotly_chart(fig, True)
                with col2:
                    fig = self.report.plot("pnl", bar=True)
                    st.plotly_chart(fig, True)
                
                fig = self.report.plot_portfolio()
                st.plotly_chart(fig)
                
            if bar == self.n:
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
        
        col1, col2, col3 = st.columns(3)
        with col1:
            symbols = st.multiselect("choose cryptocurrency ", tuple(assets), key="symbols")
        with col2:
            capital = st.number_input("capital", key="capital", min_value = 10)
        with col3:
            utc = pytz.utc
            start = st.date_input("start", key="b_start",
                                  value = datetime.datetime.now() - datetime.timedelta(days = 60),
                                  )
            end = st.date_input("end", key="b_end",
                                value = datetime.datetime.now(utc),
                                max_value = datetime.datetime.now(utc),
                                )
        run_button = st.form_submit_button("Run")
    if run_button:
        app = StApp(symbols = symbols, capital = capital,
                    start = str(start), end = str(end), interval = "1d")
        app.run()
        
                

if selected == "View":
    #s= st.session_state.start 
    #st.write(s)
    report = Report()
    
    report.run()
    col1, col2 = st.columns([1, 3])
    with col1:
        st.write(report.portfolio_data.iloc[-1]["capital"])
        st.write(report.metrics.df)
    
    with col2:
        view_f = st.selectbox("view", ("pnl", "gp", "cum_gp", "value"))
        fig = report.plot(view_f)
        st.plotly_chart(fig, True)
        
    
    symbol = st.selectbox("choose cryptocurrency ", tuple(report.symbols), key="symbol")
    fig = report.plot_asset(symbol)
    st.plotly_chart(fig, True)
    
    fig = report.plot_portfolio()
    st.plotly_chart(fig)
    st.write(" - - - ")



#streamlit run c:/Users/cc/Desktop/WcedSyst/backtest.py



