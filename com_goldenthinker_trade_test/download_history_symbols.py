from binance.client import Client
from datetime import datetime

client = Client('xoAWbPN2iKaPiGiQZ4TiFZ0yq2AvIdO4hBw8WrjA4AsFseXNbJ09Vd6wOAc8Siaw', 'Ex3dbvWjN5DgpEm960nd2M2pFz40JuqQiOVmB61X23VZEifFH0fYu6CDo7yZBvra')

# get all symbol prices
prices = client.get_all_tickers()

datetimeObject = datetime.now()
t = datetimeObject.strftime('%Y%m%d%H%M%S')




def get_klines_history():
    klines = client.get_historical_klines("BTCUSDT", Client.KLINE_INTERVAL_1MIN, "1 Jan, 2015")
    print("My klines are: "+str(klines))


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



for symbol in prices:
    s = symbol['symbol']
    p = symbol['price']
    price_history_csv_path = "D:\/historical\/binance\/realtime_" + s + ".csv"
    with open(price_history_csv_path, "a+") as price_history_file:
        print("Processing : "+str(s)+","+str(p)+"\n")
        price_history_file.write(t + "," + str(s)+","+str(p)+"\n")   