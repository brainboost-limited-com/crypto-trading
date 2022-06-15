from binance.client import Client
from datetime import datetime

client = Client('xoAWbPN2iKaPiGiQZ4TiFZ0yq2AvIdO4hBw8WrjA4AsFseXNbJ09Vd6wOAc8Siaw', 'Ex3dbvWjN5DgpEm960nd2M2pFz40JuqQiOVmB61X23VZEifFH0fYu6CDo7yZBvra')


exchange_info = client.get_exchange_info()
for s in exchange_info['symbols']:
    symbols = "com_goldenthinker_trade_telegram/symbols.txt"
    with open(symbols, "a+") as symbols_list_file:
        symbols_list_file.write(s['baseAsset']+ "/" +s['quoteAsset']+"\n")
