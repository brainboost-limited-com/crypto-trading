from binance.client import Client

client = Client('xoAWbPN2iKaPiGiQZ4TiFZ0yq2AvIdO4hBw8WrjA4AsFseXNbJ09Vd6wOAc8Siaw', 'Ex3dbvWjN5DgpEm960nd2M2pFz40JuqQiOVmB61X23VZEifFH0fYu6CDo7yZBvra')

# get all symbol prices
prices = client.get_all_tickers()
print("All symbol prices are")
print(str(prices))


history_for_symbol = client.get_order_book(symbol='BNBBTC')
print("All tickers for symbol BNBBTC are: " + str(history_for_symbol))

# get a deposit address for BTC
address = client.get_deposit_address(asset='BTC')
print("Deposit to myt address: " + str(address))



  #[
  #  1499040000000,      # Open time
  #  "0.01634790",       # Open
  #  "0.80000000",       # High
  #  "0.01575800",       # Low
  #  "0.01577100",       # Close
  #  "148976.11427815",  # Volume
  #  1499644799999,      # Close time
  #  "2434.19055334",    # Quote asset volume
  #  308,                # Number of trades
  #  "1756.87402397",    # Taker buy base asset volume
  #  "28.46694368",      # Taker buy quote asset volume
  #  "17928899.62484339" # Ignore
  # ]

klines = client.get_historical_klines("BNBBTC", Client.KLINE_INTERVAL_1WEEK, "1 Jan, 2017")
print("My klines are: "+str(klines))

tickers = client.get_ticker(symbol='BTCUSDT')
print("I got a ticket " + str(tickers))


avg_price = client.get_avg_price(symbol='BTCUSDT')
print("AVERAGE PRICE BTCUSDT " + str(avg_price))