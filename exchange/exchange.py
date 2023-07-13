import requests
import hmac
import hashlib
from urllib.parse import urljoin, urlencode
import time
from configparser import ConfigParser





def serverGap():
    path = "/fapi/v1/time"
    URL = "https://testnet.binancefuture.com"
    url = urljoin(URL, path)
    server_time = requests.get(url)
    gap = (server_time.json()['serverTime'] - time.time()*1000)/1000
    return gap

