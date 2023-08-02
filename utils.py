import requests
import hmac
import hashlib
from urllib.parse import urljoin, urlencode
import time
import datetime
from configparser import ConfigParser

import streamlit as st



@st.cache_data(ttl=60*5)
def serverGap():
    path = "/fapi/v1/time"
    URL = "https://testnet.binancefuture.com"
    url = urljoin(URL, path)
    server_time = requests.get(url)
    gap = (server_time.json()['serverTime'] - time.time()*1000)/1000
    return gap


def info():
    path = "/fapi/v1/exchangeInfo"
    URL = "https://testnet.binancefuture.com"
    url = urljoin(URL, path)
    info = requests.get(url)
    return info.json()



    
def convert(data):
    for x, y in zip(data.keys(), data.values()):
        data[x] = round(float(y), 2)
    return data

def convert2(data):
    for x in data.values():
        for y, z in zip(x.keys(), x.values()):
            if y == "updateTime":
                x[y] = convert_time(z)
            else:
                x[y] = round(float(z), 2)
    return data

def convert_time(timestamp):
    date = datetime.datetime.fromtimestamp(timestamp/1000)
    return date