import streamlit as st 
from streamlit_option_menu import option_menu

from plot import *

import datetime
import pytz


# Using object notation
add_selectbox = st.sidebar.selectbox(
    "How would you like to be contacted?",
    ("Email", "Home phone", "Mobile phone")
)

# Using "with" notation
with st.sidebar:
    st.radio("page", ["simulation", "futures"])
    

# streamlit run c:/Users/cc/Desktop/WcedSyst/dash.py