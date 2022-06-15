from binance.client import Client
from datetime import datetime

client = Client('xoAWbPN2iKaPiGiQZ4TiFZ0yq2AvIdO4hBw8WrjA4AsFseXNbJ09Vd6wOAc8Siaw', 'Ex3dbvWjN5DgpEm960nd2M2pFz40JuqQiOVmB61X23VZEifFH0fYu6CDo7yZBvra')

# get all symbol prices
prices = client.get_all_tickers()

datetimeObject = datetime.now()
t = datetimeObject.strftime('%Y%m%d%H%M%S')


for symbol in prices:
    s = symbol['symbol']
    p = symbol['price']
    price_history_csv_path = "historical_data/realtime_" + s + ".csv"
    with open(price_history_csv_path, "a+") as price_history_file:
        print("Processing : "+str(s)+","+str(p)+"\n")
        price_history_file.write(t + "," + str(s)+","+str(p)+"\n")   