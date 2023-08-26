import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

import streamlit as st 
from streamlit_option_menu import option_menu
import multiprocessing

import os
import datetime
import pytz
from sqlalchemy import create_engine

from app.report import Report
from app.simulation import Simulation
from utils import assets



class StApp(Simulation):
    
    def __init__(self, symbols, capital, interval = "1d", start="2023", end="2023", db_trades = "simulation_"):
        Simulation.__init__(self, symbols = symbols, capital = capital,
                     interval = interval, start = start, end = end, db_trades = db_trades)
    
    def run(self):
        
        self.portfolio.config(m = 3, floor = 0)
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
            self.monitoring.run(trades = data, portfoliodf = portfolio_data)
            
            with placeholder.container():
                #n=
                symbols = self.symbols
                cols = st.columns(len(symbols)+1)
                
                with cols[0]:
                    capital = self.portfolio.init_capital
                    st.metric("Balance", capital, delta=(portfolio_data.capital.iloc[-1] - capital))

                for i, symbol in enumerate(symbols):
                    with cols[i+1]:
                        value_i = self.assets[symbol].in_value
                        pnl = self.assets[symbol].pnl
                        st.metric(label=symbol, value = value_i, delta = pnl)
                
                with st.expander("asset", True):
                    #ticker = st.radio(label="-", options=symbols, horizontal=True, key="tick")
                    fig = self.monitoring.plot_asset(symbols[0])
                    st.plotly_chart(fig, True)
                    
                col1, col2 = st.columns(2)
                with col1:
                    fig = self.monitoring.plot("pnl", bar=True)
                    st.plotly_chart(fig, True)
                with col2:
                    st.subheader("Position")
                    df = data.drop(columns=["position", "status", "out_value"]).copy()
                    
                    for symbol in st.session_state["symbols"]:
                        df_ = df[df["symbol"] == symbol].copy()
                        df_.set_index("symbol", inplace=True)
                        df_.dropna(inplace = True)
                        st.table(df_.iloc[-1:])
                
                fig = self.monitoring.plot_portfolio()
                st.plotly_chart(fig, True)

            if bar == self.n:
                break
        self.journal.save_data()


def config(simulation):
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
    return symbols, capital, start, end

path = os.getcwd() + "\\data"
simulation_list = os.listdir(path)
if len(simulation_list) == 0:
    simulation_list.append("")

col1, col2 = st.columns([1, 3])
with col1:
    sim = option_menu(
                menu_title=None, 
                options=simulation_list,
                orientation="vertical"
                )
    clear = st.button("delete")
    if clear:
        os.remove(path+f"\\{sim}")
        
with col2:
    ""


st.title("Simulation")
selected = option_menu(
                    menu_title=None, 
                    options=["Run", "Run_Portfolio", "Reading"],
                    icons=["pencil-fill", "bar-chart-fill"],
                    orientation="horizontal"
                    )


if selected == "Run":
    st.write("Run a Simulation")
    with st.form("config"):
        simulation_name = st.text_input("simulation-desciption", "simulation_")
        symbols, capital, start, end = config(simulation_name)
        run_button = st.form_submit_button("Run")
        
    if run_button:
        app = StApp(symbols = symbols, capital = capital,
                    start = str(start), end = str(end), interval = "1d", db_trades = simulation_name)
        app.run()







class MApp(Simulation):
    
    def __init__(self, symbols, capital, interval = "1d", start="2023", end="2023", db_trades = "simulation_"):
        Simulation.__init__(self, symbols = symbols, capital = capital,
                     interval = interval, start = start, end = end, db_trades = db_trades)
    
    def run(self):
        self.portfolio.config(m = 3, floor = 0)
        self.set_assets()
        
        bar = 1
        bar_p = 0
        
        placeholder = st.empty()
        progress_bar = st.progress(0)
        st.write(" --- ---- ---")
        while True:
            
            self.apply(bar)
            bar += 1
            with placeholder.container():
                bar_p = (self.n - bar)/self.n
                progress_bar.progress(bar_p)
                
                data = self.journal.data
                portfolio_data = self.journal.portfolio_data
                
                self.report.run(data, portfolio_data)
                
                st.write(f"{bar} / {self.n}")
            if bar == self.n:
                break


def run_simulation(params):
        app = MApp(**params)
        app.run()

if selected == "Run_Portfolio":
    st.write("Faire une simulation de plusieur portfolio")
    
    portfolios = {}
    with st.form("config"):
        simulation_id = st.text_input("simulation-desciption", "simulation_")
        symbols, capital, start, end = config(simulation_id)
        
        add_button = st.form_submit_button("Add")
        
    if add_button:
        portfolios[simulation_id] = {"symbols" : symbols, "capital" : capital,
                                     "start" : start, "end" : end}
        st.success("done")
    # save file.yaml
    
    with st.expander("Before simulation"):
        st.write(portfolios)
    
    with st.form("Run"):
        portfolio_params = [
            {"symbols": ["ETH"], "capital": 100, "start": "2023-01", "end": "2023-04", "interval": "1d", "db_trades": "P1"},
            {"symbols": ["XMR"], "capital": 100, "start": "2023-01", "end": "2023-04", "interval": "1d", "db_trades": "P2"}
        ]
        st.write(portfolio_params)
        run_button = st.form_submit_button("Run")
    
    if run_button:
        processes = []
        for params in portfolio_params:
            p = multiprocessing.Process(target=run_simulation, args=(params,))
            processes.append(p)
            p.start()
                
        for p in processes:
            p.join()
        

#n=





