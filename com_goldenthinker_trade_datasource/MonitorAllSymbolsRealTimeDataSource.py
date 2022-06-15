
from com_goldenthinker_trade_datasource.RealTimeDataSource import RealTimeDataSource

from com_goldenthinker_trade_exchange.ExchangeConfiguration import ExchangeConfiguration
from com_goldenthinker_trade_logger.Logger import Logger
from requests import get
from com_goldenthinker_trade_datainput.DataInputManager import DataInputManager
from decimal import Decimal
import os
import sys


class MonitorAllSymbolsRealTimeDataSource(RealTimeDataSource):
    
    
    def __init__(self):
        super().__init__('gt_monitor_all_symbols', trust=Decimal(0.99999999), session=self)
        self.server_ip = get('https://api.ipify.org').text
        #DataInputManager.get_input('logger').input("Monitoring all symbols from server ec2-user@" + str(self.server_ip),{'telegram':True})
       

    def start(self):
        try:
            from com_goldenthinker_trade_datasource_network.TickerSocketAllSymbols import TickerSocketAllSymbols
            my_ticker_socket = TickerSocketAllSymbols(exchange=ExchangeConfiguration.get_default_exchange())
            my_ticker_socket.start()
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            print(str(e))
            #DataInputManager.get_input('logger').input("Monitoring all symbols from server ec2-user@" + str(self.server_ip) + " stopped due to error.",{'telegram':True})