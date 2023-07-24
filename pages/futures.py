import streamlit as st
from streamlit_option_menu import option_menu
from streamlit_autorefresh import st_autorefresh
import calendar
import datetime
import time
import json
from collections import deque, defaultdict

from utils import *

from app.plot import *
from app.exchange.order import Order

from data.crm import DCRM

from app.exchange.portfolio import Portfolio
from app.exchange.utils import serverGap

import warnings
warnings.filterwarnings('ignore')


# ---- Page Config --- 
st.set_page_config(
    page_title="W - Binance",
    page_icon=":money_with_wings:",
    layout="wide"
)


# ------------------ Data -----------------

@st.cache_data(ttl=60*10)
def update_portfolio():
    portfolio = Portfolio()
    portfolio.futureAccountInfo()

    wallet = portfolio.wallet
    wallet = convert(wallet)
    assets = portfolio.assets
    positions = portfolio.positions
    positions = convert2(positions)
    
    SYMBOLS =  list(positions.keys())
    df = pd.DataFrame()
    for i, symbol in enumerate(SYMBOLS):
        add = pd.DataFrame(positions[symbol], index=[symbol])
        df = df.append(add)
    
    return wallet, positions, df, True

wallet, positions, df, p_updated = update_portfolio()
ORDER_SYMBOLS = df.index.to_list()

TICKERS_MARGIN = defaultdict(float)
for symbol in ORDER_SYMBOLS:
    TICKERS_MARGIN[symbol] = positions[symbol]["initialMargin"]

nb_tickers = len(ORDER_SYMBOLS)

dcrm = DCRM()

#  ----------- Progress bar ----------
#bar = st.progress(0)
now = datetime.datetime.now()
st.write(now.strftime("%H:%M:%S"))

refresh_int = 10 * 60 * 1000
st_autorefresh(interval=refresh_int, key="autorefresh")

bar_2 = st.progress(0)
if p_updated:
    start = time.time()
    gap_time = time.time() - start
    gap_time = min(gap_time, 10000)
    gap_time = (10000 - gap_time)/10000
    c_refresh = st.session_state.autorefresh
    bar_2.progress(gap_time)
    



st.title("Binance")

# -- Server Gap --
server_gap = serverGap()
st.write("server time gap ",server_gap)

# ------------------ Account -----------------
st.title("Account")
with st.container():
    
    col1, col2, col3, col4 = st.columns([1, 1, 1, 3])
    with col1:
        st.metric(label="Margin Balance", value=wallet["totalMarginBalance"])
        st.metric(label="Avalaible Balance", value=wallet["avaibleBalance"])
        st.metric(label="Position Margin", value=wallet["totalPositionInitialMargin"])
        st.metric(label="Order Margin", value=wallet["totalOpenOrderInitialMargin"])

    with col2:
        st.metric(label="Margin Balance", value=wallet["totalMarginBalance"])
        st.metric(label="Wallet Balance", value=wallet["totalWalletBalance"], delta=wallet["totalUnrealizedProfit"])
        st.metric(label="Unrealised PNL", value= wallet["totalUnrealizedProfit"])
        
    with col3:
        st.metric(label="Init Margin", value=wallet["totalInitialMargin"])
        st.metric(label="Position Init Margin", value=wallet["totalPositionInitialMargin"])
        st.metric(label="Order Init Margin", value=wallet["totalOpenOrderInitialMargin"])
    
    with col4:
        fig = sunburst(MarginBalance= wallet["totalMarginBalance"],
                         AvalaibleBalance=wallet["avaibleBalance"],
                       PositionMargin=wallet["totalPositionInitialMargin"], 
                       OrderMargin=wallet["totalOpenOrderInitialMargin"],
                       Margin= TICKERS_MARGIN)
        st.plotly_chart(fig, True)

# --- Plot Portfolio ---
with st.expander('Graphique'):
    st.write("Total Margin Evolution")
    st.write("Wallet Balance")




st.title("Order")
placeholder = st.empty()
base = "USDT"
with st.expander("Place Order"):
    with st.form("order"):
        col1, col2, col3 = st.columns(3)
        with col1:
            symbol = st.selectbox("symbol", ["BTC", "SOL", "ETH", "DASH", "QNT"], index=0)
        with col2:
            quantity = st.number_input("quantity", key="quantity")
        with col3:
            leverage = st.slider("leverage", min_value=1, max_value=50, key="leverage")
        recvWindow = st.slider(label="recvWindow", min_value=0, max_value=60, value=10)
        set_order = option_menu(menu_title="Set Order", 
                                options=["BUY/LONG", "SELL/SHORT"],
                                orientation="horizontal", key="set_order")
        execute = st.form_submit_button("Execute")
        
    order = Order(symbol = symbol+base, recvWindow=recvWindow*1000)
    st.write("Interval : ",order.recvWindow)
    meta = ""
    if execute:
        lev = order.leverage(leverage)
        col1, col2 = st.columns([1, 3])
        with col1:
            if set_order == "LONG":
                meta = order.buy(quantity)
                st.success("Send")
                #dcrm.add_data()
                    
            if set_order == "SHORT":
                meta = order.sell(quantity)
                st.success("Send")
        with col2:
            st.write("Leverage : \n",lev.json())
            st.write("Order : \n",meta.json())

        col1, col2 = st.columns(2)
        with placeholder:
            with col1:
                Close = st.button("Close")
            with col2:
                CloseAll = st.button("Close All", help="Close all positions")





st.title("Position")
with st.expander("View All positions"):
    st.dataframe(df)

def bullet_data(symbol):
    data = df.copy()
    data_dict = {
        "symbol" : symbol,
        "size" : data.loc[symbol, "size"],
        "initialMargin" : data.loc[symbol, "initialMargin"],
        "positionInitialMargin" : data.loc[symbol, "positionInitialMargin"],
        "openOrderInitialMargin" : data.loc[symbol, "openOrderInitialMargin"],
        "unrealizedProfit" : data.loc[symbol, "unrealizedProfit"],
        
        "quantity" : data.loc[symbol, "positionAmt"],
        "entryPrice" : data.loc[symbol, "entryPrice"],
        "markPrice" : data.loc[symbol, "markPrice"],
        "liquidationPrice" : data.loc[symbol, "liquidationPrice"],
        "notional" : data.loc[symbol, "notional"],
        
    }
    return data_dict

y = np.array([
    [0.05, 0.3],
    [0.35, 0.6],
    [0.65, 0.9]
])

col1, col2, col3 = st.columns(3)
with col1:
    fig = go.Figure()
    for i in range(nb_tickers):    
        data_dict = bullet_data(ORDER_SYMBOLS[i])
        bulletChart(fig, data_dict, list(y[i]))        
    st.plotly_chart(fig)


clear_cache = st.button("clear cache")
if clear_cache:
    update_portfolio.clear()

#streamlit run c:/Users/cc/Desktop/WcedSyst/futures.py
