from com_goldenthinker_trade_strategy.Strategy import Strategy
import time
from com_goldenthinker_trade_model.Symbol import Symbol
from com_goldenthinker_trade_exchange.ExchangeConfiguration import ExchangeConfiguration


from com_goldenthinker_trade_exchange.ExchangeConfiguration import ExchangeConfiguration
from com_goldenthinker_trade_datatype.CryptoFloat import CryptoFloat
from com_goldenthinker_trade_monitor.SymbolMonitor import SymbolMonitor

import threading

class Ticker:
    
    _instance = None
    _is_running = False
    _all_tickers = None

    
    @classmethod
    def instance(cls):
        if cls._instance is None:
            cls._instance = cls.__new__(cls)
            cls._instance.symbol_monitors = dict()
        cls._instance.exchange = ExchangeConfiguration.get_default_exchange()
        return cls._instance
        
        
    def get_all_tickers(self):
        self.__class__._is_running = True
        tickers = dict()
        my_tickers = self.exchange.get_all_tickers()
        [tickers.__setitem__(x['symbol'],float(x['price'])) for x in my_tickers]
        self.__class__._all_tickers = tickers
        return tickers
        
    def add_listener_monitor(self,symbol_monitor):
        self.__class__._instance.symbol_monitors[symbol_monitor.get_symbol().uppercase_format()] = symbol_monitor
    
    
    def notify_monitors(self):
        symbols_to_notify = self.__class__._instance.symbol_monitors.values()
        for monitor in symbols_to_notify:
            monitor.tick(self.__class__._all_tickers[monitor.get_symbol().uppercase_format()])
            
    def start(self):
        while True:
            time.sleep(10)
            self.get_all_tickers()
            self.notify_monitors()
    
        
        