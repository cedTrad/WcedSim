

assets = ['USDT', 'BTC', 'ETH', 'EGLD', 'QNT', 'BNB', 'KSM', 'XMR', 'AAVE']


Assets = ['USDT', 'BTC', 'ETH', 'SOL', 'EGLD', 'VET', 'GALA', 'QNT', 'TWT', 'BNB', 'KSM',
          'XMR', 'MATIC', 'DOT', 'SHIB', 'AAVE', 'FET', 'OCEAN', 'SC', 'CELR',
          'LINK', 'XRP', 'ADA', 'LTC', 'AVAX', 'ATOM', 'FIL', 'NEAR', 'ICP', 'ALGO',
          'FTM', 'THETA', 'CHZ', 'NEO', 'DASH', 'SNX', 'KAVA', 'DOGE', 'SAND',
          'CRV', 'ZIL', 'CELO', 'BAT', 'XLM', 'DODO', 'IOTA', 'APT', 'TROY', 'REN', 'IDEX',
          'YFI', 'EOS', 'LUNC', 'CFX', 'OP', 'LDO', 'PAXG', 'TRX', 'ILV', 'CAKE',
          'DEXE', 'ETC', 'LIT', 'APE', 'LTO', 'HOT', 'AXS', 'COMP', 'LUNA',
          'CFX', 'IMX', 'WOO', 'MINA', 'PEPE', 'ARB', 'MANA']


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