from com_goldenthinker_trade_datasource_network.TickerSocketAllSymbols import TickerSocketAllSymbols
from com_goldenthinker_trade_exchange.ExchangeConfiguration import ExchangeConfiguration
from com_goldenthinker_trade_logger.Logger import Logger
from requests import get

server_ip = get('https://api.ipify.org').text

Logger.log("Monitoring all symbols from server goldenthinker@" + str(server_ip),telegram=True)

try:
    my_ticker_socket = TickerSocketAllSymbols(exchange=ExchangeConfiguration.get_default_exchange())
    my_ticker_socket.start()
except:
    Logger.log("Monitoring all symbols from server goldenthinker@" + str(server_ip) + " stopped due to error.",telegram=True)