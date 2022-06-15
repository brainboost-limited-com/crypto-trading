from decimal import Decimal
from com_goldenthinker_trade_datasource_network.TickerSocketMultipleSymbols import TickerSocketMultipleSymbols

from com_goldenthinker_trade_logger.Logger import Logger
from com_goldenthinker_trade_datasource.RealTimeDataSource import RealTimeDataSource


class MonitorSpecificSymbolsRealTimeDataSource(RealTimeDataSource):
    
    def __init__(self,symbol='',trust=Decimal(0.9999999), order=None, session=None,consumers=[],thread_name=''):
        super().__init__(name='monitor_symbol_'+symbol.uppercase_format(),trust=trust,session=session,consumers=consumers)
        self.name = 'monitor_symbol_'+str(symbol.uppercase_format())
        self.symbols_to_monitor = [symbol.uppercase_format()]
        from com_goldenthinker_trade_exchange.ExchangeConfiguration import ExchangeConfiguration
        self.my_ticker_socket = TickerSocketMultipleSymbols(exchange=ExchangeConfiguration.get_default_exchange(),symbols=self.symbols_to_monitor)
        self.thread_name=thread_name
        Logger.log("Executing MonitorSpecificSymbolsRealTimeDataSource constructor from thread " + self.thread_name)
        
        if order is not None:
            self.consumers.append(order)


        
    def start(self):
        Logger.log("Executing MonitorSpecificSymbolsRealTimeDataSource().start() method from thread " + self.thread_name)
        self.my_ticker_socket.start()
    
    def notify(self,data):
        print("MONITOR_SYMBOL_INDIVIDUALLY: " + str(data))    
    
        
    