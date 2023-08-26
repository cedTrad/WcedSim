import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

import streamlit as st 
from streamlit_option_menu import option_menu

import datetime
import pytz
from sqlalchemy import create_engine
import os

from app.report import Report
from app.simulation import Simulation
from utils import assets

import warnings
warnings.filterwarnings('ignore')


st.set_page_config(page_title="Trading System",
                    page_icon=":female-doctor",
                    layout="wide")


st.title("Analytics")


path = os.getcwd() + "\\data"
simulation_list = os.listdir(path)

with st.expander("Description"):
    col1, col2 = st.columns([1, 3])
    with col1:
        simulation_select = option_menu(
                                menu_title=None, 
                                options=simulation_list,
                                icons=["pencil-fill", "bar-chart-fill"],
                                orientation="vertical"
                                )
        report = Report(db_trades = simulation_select)
        report.run()
        
    with col2:
        st.table(report.symbols)


symbols = report.symbols
#st.table(symbols)

tab_1, tab_2, tab_3, tab_4, tab_5 = st.tabs(["Global", "Portfolio", "Asset", "PnL Analysis", "Risk"])


tab_1.subheader("Global Overviews")
with tab_1:
    symbols = report.symbols
    cols = st.columns(4)
    with cols[0]:
        p_data = report.portfolio_data
        capital = p_data.iloc[0]["capital"]
        st.metric("Balance", capital, delta=(p_data.iloc[-1]["capital"] - p_data.iloc[0]["capital"]))
    
    with cols[1]:
        st.metric("Drawdown", 10)
        
    with cols[2]:
        st.metric("Long", 5)
        
    with cols[3]:
        st.metric("Short", 1)

tab_1_1, tab_1_2 = tab_1.tabs(["Views", "distribution"])
select_view = tab_1_1.selectbox("view", ("pnl", "gp", "cum_gp", "value"))
fig = report.plot(select_view)
tab_1_1.plotly_chart(fig, True)
    
    
    
tab_2.subheader("Portfolio Performance with more details")
fig = report.plot_portfolio()
tab_2.plotly_chart(fig, True)

fig = report.p_evalutation.plot()
tab_2.plotly_chart(fig, True)

with tab_2:
    col1, col2 = st.columns(2)
    with col1:
        fig = report.viz_portfolio_dist()
        st.plotly_chart(fig, True)
    with col2:
        st.write("ff")



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
    


