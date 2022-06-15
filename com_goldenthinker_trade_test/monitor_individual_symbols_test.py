from com_goldenthinker_trade_datasource_network.TickerSocketMultipleSymbols import TickerSocketMultipleSymbols
from com_goldenthinker_trade_exchange.ExchangeConfiguration import ExchangeConfiguration


symbols_to_monitor = ['BTCUSDT','ETHUSDT']


my_ticker_socket = TickerSocketMultipleSymbols(exchange=ExchangeConfiguration.get_default_exchange(),symbols=symbols_to_monitor)


my_ticker_socket.start()

