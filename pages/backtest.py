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
    
    def __init__(self, symbols, capital, interval = "1d", start="2023", end="2023", db_trades = "simulation_"):
        Simulation.__init__(self, symbols = symbols, capital = capital,
                     interval = interval, start = start, end = end, db_trades = db_trades)
    
    def run(self):
        
        self.portfolio.config(m = 3.5, floor = 0)
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
                st.plotly_chart(fig, True)
                
            if bar == self.n:
                break

   
simulation_select = st.sidebar.selectbox(" Select Simulation", [f"simulation_{i}" for i in range(1, 10)])

SYMBOLS = ['BTC', 'ETH', 'DASH']
        
st.title("Simulation")


selected = option_menu(
                    menu_title=None, 
                    options=["View", "Run"],
                    icons=["pencil-fill", "bar-chart-fill"],
                    orientation="horizontal"
                    )

if selected == "Run":
    st.title("Simulation")
    with st.form("config"):
        simulation_name = st.text_input("simulation-desciption", "simulation_")
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
                    start = str(start), end = str(end), interval = "1d", db_trades = simulation_name)
        app.run()




if selected == "View":
    st.title("Analytics")
    
    report = Report(db_trades = simulation_select)
    report.run()
    #indicateur = report.metrics.df.T    
    tab_1, tab_2, tab_3, tab_4, tab_5 = st.tabs(["Global", "Portfolio", "Asset", "PnL Analysis", "Risk"])
    tab_1.subheader("Global Overviews")
    #tab_1.table(indicateur.applymap(lambda x : "{:.{}f}".format(x, 2)))
    
    
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
    
    with tab_4:
        col1, col2 = st.columns(2)
        with col1:
            fig = report.pnl.viz_distribution(symbol_pnl)
            st.plotly_chart(fig, True)
        with col2:
            fig = report.pnl.viz_distribution(symbol_pnl)
            st.plotly_chart(fig, True)
        #metrics = tab_4.selectbox("choose metrics", ["total_pnl", "expentancy", "profit_factor"])
        metrics = tab_4.multiselect("choose metrics", ["avg_gp" ,"total_pnl", "expentancy", "profit_factor", "win_rate", "loss_rate"])
        fig = report.pnl.plot_metric(symbol_pnl, metrics)
        st.plotly_chart(fig, True)
        
        
            
        
    
    tab_5.subheader("Risk Analysis")
    tab_5.plotly_chart(report.plot_cppi())
    
# streamlit run c:/Users/cc/Desktop/WcedSyst/backtest.py



