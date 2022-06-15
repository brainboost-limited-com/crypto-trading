from abc import ABC, abstractmethod
from com_goldenthinker_trade_logger.Logger import Logger
from com_goldenthinker_trade_monitor.Tick import Tick

from com_goldenthinker_trade_monitor.SymbolMonitor import SymbolMonitor
from datetime import datetime, timedelta

class Ticker(ABC):
    
    _last_tick_timestampt = datetime.now()
    _reset_socket = False
    
    def __init__(self,exchange=None,symbols=None):
        self.monitors = dict()
        self.current_ticks = []
        if exchange is None:
            from com_goldenthinker_trade_exchange.ExchangeConfiguration import ExchangeConfiguration
            self.exchange = ExchangeConfiguration.get_default_exchange()
        else:
            self.exchange = exchange
        
        
            
            
            
    def subscribe(self,monitor):
        self.monitors[monitor.get_symbol().uppercase_format()] = monitor
        
    def on_tick(self,data=[]):
        if type(data)==Tick:
            self.notify(data.to_dict())
        else:
            self.notify(data['data'])
            while ((datetime.now() - Ticker._last_tick_timestampt) < timedelta(seconds=3)):
                print("waiting.. reconnecting socket..")
            if ((datetime.now() - Ticker._last_tick_timestampt) >= timedelta(seconds=3)):
                self.restart()
        
    
        
        
    def notify(self,data=[]):
        if 'list' in str(type(data)):
            for t in data:
                tick = Tick(t)
                try:
                    self.monitors[str(tick.get_symbol())].tick(tick)
                except:
                    Logger.log("The symbol " + str(tick.get_symbol()) + " does not exist, update symbols database.")
                    pass
        else:
            try:
                if 'dict' in str(type(data['data'])):
                    tick = Tick(data['data'])
                    self.monitors[str(tick.get_symbol())].tick(tick)
            except:
                Logger.log("The symbol " + str(tick.get_symbol()) + " does not exist, update symbols database.")
                pass
        
            
    
    def restart(self):
        self.start()
            
    @abstractmethod
    def start(self):
        pass