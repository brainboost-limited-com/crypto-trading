
from com_goldenthinker_trade_datasource_network.Ticker import Ticker
from com_goldenthinker_trade_model.Symbol import Symbol
import traceback
from com_goldenthinker_trade_monitor.SymbolMonitor import SymbolMonitor

class TickerSocketMultipleSymbols(Ticker):
    
    def __init__(self, exchange, symbols, callback=None):
        super().__init__(exchange=exchange, symbols=symbols)
        self.callback = callback
        if len(symbols) >= 1:
            self.monitors = dict()
            for s in symbols:
                self.subscribe(SymbolMonitor(Symbol(s)))
                
    
    def on_tick(self,data=[]):
        try:
            self.notify(data)
            if self.callback != None:
                self.callback(data,self.get_current_sequence(symbol=data['data']['s']))
        except Exception as e:
            traceback.print_exc()
            print(str(e))
            
    

    def get_current_sequence(self,symbol):
        return self.monitors[symbol].get_current_sequence()

                
    def start(self):
        self.exchange.subscribe_multiple_individual_symbols(callback=self.on_tick,symbols=[m for m in self.monitors.keys()])
