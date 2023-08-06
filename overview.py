import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

import streamlit as st 
from streamlit_option_menu import option_menu

import datetime
import pytz


st.set_page_config(
    page_title="Overview",
    page_icon=":money_with_wings:",
    layout="wide"
)

st.title("OverViews")

with st.sidebar:
    
    st.write("hello")




data_df = pd.DataFrame(
    {
        "indicator": [30, 70],
    }
)

st.data_editor(
    data_df,
    column_config={
        "indicator": st.column_config.ProgressColumn(
            "Rate Return",
            help="Win Rate",
            format="%f",
            min_value=0,
            max_value=100,
        ),
    },
    hide_index=True,
)


# streamlit run c:/Users/cc/Desktop/CedAlgo/WcedSim/overview.py






