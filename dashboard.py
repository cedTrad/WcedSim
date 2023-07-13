import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

import streamlit as st 
from streamlit_option_menu import option_menu

from report import Report
from sqlalchemy import create_engine


from app import App

import warnings
warnings.filterwarnings('ignore')


Assets = ['BTC', 'ETH', 'SOL', 'EGLD', 'VET', 'GALA', 'QNT', 'TWT', 'BNB', 'KSM',
          'XMR', 'MATIC', 'DOT', 'SHIB', 'AAVE', 'FET', 'OCEAN', 'SC', 'CELR',
          'LINK', 'XRP', 'ADA', 'LTC', 'AVAX', 'ATOM', 'FIL', 'NEAR', 'ICP', 'ALGO',
          'FTM', 'THETA', 'CHZ', 'NEO', 'DASH', 'SNX', 'KAVA', 'DOGE', 'SAND',
          'CRV', 'ZIL', 'CELO', 'BAT', 'XLM', 'DODO', 'IOTA', 'APT', 'TROY', 'REN', 'IDEX',
          'YFI', 'EOS', 'LUNC', 'CFX', 'OP', 'LDO', 'PAXG', 'TRX', 'ILV', 'CAKE',
          'DEXE', 'ETC', 'LIT', 'APE', 'LTO', 'HOT', 'AXS', 'COMP', 'LUNA',
          'CFX', 'IMX', 'WOO', 'MINA', 'PEPE', 'ARB', 'MANA']


class DashBoard:
    
    def __init__(self):
        st.set_page_config(page_title="Trading System",
                           page_icon=":female-doctor",
                           layout="wide")
        
        st.title("------ Backtesting -------")
        
        self.engine = create_engine(f"sqlite:///database/data.db")
        
        
    def app_config(self, symbols, capital):
        self.symbols = symbols
        self.app = App(symbols, capital)
    
    def plot_portfolio(self):
        fig = self.report.plot_portfolio()
        st.plotly_chart(fig)
    
    def plot_asset(self, symbol, asset):
        fig = self.report.plot_asset(symbol, asset)
        st.plotly_chart(fig)
    
    def add_sidebar(self):
        st.sidebar.header("Menu")
    
    def run_app(self):
        self.app.run()
    
    def get_report(self, update):
        if update is True:
            self.run_app()
            self.report = self.app.report
        else:
            data = pd.read_sql("trades", self.engine)
            portfolio_data = pd.read_sql("portfolio_tab", self.engine)
            report = Report()
            self.report = report.run(data, portfolio_data)


    def run(self):
        
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
                    symbols = st.multiselect("choose cryptocurrency ", tuple(Assets))
                with col2:
                    capital = st.number_input("capital")
                self.app_config(symbols, capital)
                
                run_button = st.form_submit_button("Run")
                
                if run_button:
                    st.write("state : ",run_button)
                    self.get_report(update = True)
                
                self.plot_portfolio()
            
        if selected == "View":
            self.get_report(update = False)
            st.write(self.report)
        
            
    

dd = DashBoard()
dd.run()

#streamlit run c:/Users/cc/Desktop/W/dashboard.py


