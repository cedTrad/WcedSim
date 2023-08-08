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


st.title("Analytics")

simulation_select = st.sidebar.selectbox(" Select Simulation", [f"simulation_{i}" for i in range(1, 10)])
st.sidebar.title("Description")

file = st.file_uploader("simulation")


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
    


