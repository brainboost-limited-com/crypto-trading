from com_goldenthinker_trade_exchange.ExchangeConfiguration import ExchangeConfiguration
from binance.client import Client


API_KEY = 'xoAWbPN2iKaPiGiQZ4TiFZ0yq2AvIdO4hBw8WrjA4AsFseXNbJ09Vd6wOAc8Siaw'
API_SECRET = 'Ex3dbvWjN5DgpEm960nd2M2pFz40JuqQiOVmB61X23VZEifFH0fYu6CDo7yZBvra'

client = Client(API_KEY,API_SECRET)


info = client.futures_exchange_info()
pricePrecision = info['symbols'][0]['pricePrecision']
quantityS = 10.10
quantity = "{:0.0{}f}".format(quantityS, pricePrecision)


client.create_order(symbol='BTCUSDT',side=Client.SIDE_BUY,type=Client.ORDER_TYPE_MARKET,quantity=quantity)
