from binance_client import BinanceClient
from trading_algorithm import TradingAlgorithm

client = BinanceClient(api_key='your_api_key', api_secret='your_api_secret')
symbols = ['BTCUSDT', 'ETHUSDT', 'BNBUSDT']
algorithm = TradingAlgorithm()

while True:
    prices = client.get_symbol_prices(symbols)
    signals = algorithm.generate_signals(prices)
    orders = algorithm.generate_orders(signals, prices)
    client.execute_orders(orders)