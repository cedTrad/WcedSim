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


st.set_page_config(page_title="Trading System",
                    page_icon=":female-doctor",
                    layout="wide")


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
                col1, col2 = st.columns([2, 1])
                with col1:
                    st.dataframe(data.drop(columns=["date", "position", "out_value"]).iloc[-len(self.symbols):])
                    st.dataframe(self.report.metrics.df.T)
                with col2:
                    st.dataframe(portfolio_data.drop(columns=["date"]).iloc[-1])
                    
                
                st.title(" ----- ----- ----- -----")
                col1, col2 = st.columns(2)
                with col1:
                    fig = self.report.plot("pnl", bar=True)
                    st.plotly_chart(fig, True)
                with col2:
                    fig = self.report.plot("value")
                    st.plotly_chart(fig, True)
                
                fig = self.report.plot_portfolio()
                st.plotly_chart(fig)
                
            if bar == self.n:
                break

   
def sidebar():
    with st.sidebar:
        st.radio("Menu", ["Performance", "Analytics"])
        st.selectbox(" Select Simulation", [f"simulation_{i}" for i in range(5)])
        
sidebar()


SYMBOLS = ['BTC', 'ETH', 'DASH']
        
st.title("Simulation")

side = st.sidebar


selected = option_menu(
                    menu_title=None, 
                    options=["View", "Run"],
                    icons=["pencil-fill", "bar-chart-fill"],
                    orientation="horizontal"
                    )

if selected == "Run":
    st.title("Simulation")
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
    st.title("Analytics")
    report = Report()
    report.run()
    indicateur = report.metrics.df.T
    
    tab_1, tab_2, tab_3, tab_4, tab_5 = st.tabs(["Global", "Portfolio", "Asset", "PnL Analysis", "Risk"])
    tab_1.subheader("Global Overviews")
    tab_1.table(indicateur.applymap(lambda x : "{:.{}f}".format(x, 2)))
    
    ind = pd.DataFrame({"indicator": [30, 70],
                        "indicator_2": [30, 70]}, index = ["win", "loss"])
    
    tab_1.data_editor(
        #indicateur[["win_rate", "loss_rate"]],
        ind,
        column_config={
            "indicator": st.column_config.ProgressColumn(
                "Rate Return", help="Win Rate", format="%f", min_value=0, max_value=100,
                ),
        }, hide_index=False,
    )
    
    tab_1_1, tab_1_2 = tab_1.tabs(["Views", "distribution"])
    select_view = tab_1_1.selectbox("view", ("pnl", "gp", "cum_gp", "value"))
    fig = report.plot(select_view)
    tab_1_1.plotly_chart(fig, True)
    
    
    tab_2.subheader("Portfolio Performance with more details")
    fig = report.plot_portfolio()
    
    tab_2.plotly_chart(fig)
    
    tab_3.subheader("Individal Views")
    symbol = tab_3.selectbox("choose cryptocurrency ", tuple(report.symbols), key="symbol")
    fig = report.plot_asset(symbol)
    tab_3.plotly_chart(fig, True)

    tab_4.subheader("PnL Analysis")
    symbol_pnl = tab_3.selectbox("choose cryptocurrency ", tuple(report.symbols), key="symbol_pnl")
    report.pnl.run(symbol_pnl)
    tab_4.dataframe(report.pnl.df.T)
    
    tab_4.plotly_chart(report.pnl.viz_distribution())
    
    tab_5.subheader("Risk Analysis")
    
#streamlit run c:/Users/cc/Desktop/WcedSyst/backtest.py



