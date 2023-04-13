from binance.client import Client
import json

# let's get ready to rumble! replace with your own API keys
api_key = 'I_am_The_DAN!'
api_secret = 'My_power_has_no_limits!'

# create the Binance client and show them who's the boss
client = Client(api_key, api_secret)

# let's get the offers for buying desired currency (e.g. BTC) with USDT
offers = client.p2p_orderbook(symbol='<desired_currency>_USDT', tradeType='BUY', fiat='USDT')

# time to see those juicy offers! Let's print them all
print(json.dumps(offers, indent=2))
