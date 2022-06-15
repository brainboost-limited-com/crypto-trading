from com_goldenthinker_trade_logger.Logger import Logger
from com_goldenthinker_trade_datasource_network.Ticker import Ticker


class TickerSocketAllSymbols(Ticker):
    
    def __init__(self, exchange,symbols=None, local_source=False):
        super().__init__(exchange=exchange, symbols=None)
        self.local_source = local_source
        from com_goldenthinker_trade_exchange.ExchangeConfiguration import ExchangeConfiguration
        all_symbols_monitors = ExchangeConfiguration.get_default_exchange().get_list_of_symbols()
        
        for sm in all_symbols_monitors:
            Logger.log("Creating monitor for symbol " + sm.uppercase_format())
            
            from com_goldenthinker_trade_monitor.SymbolMonitor import SymbolMonitor
            from com_goldenthinker_trade_model.Symbol import Symbol
            create_symbol_monitor = SymbolMonitor(sm)
            
            self.subscribe(create_symbol_monitor)
        
        
        
    def start(self):
        if self.local_source==False:
            Logger.log("Monitoring all symbols from network socket")
            self.exchange.subscribe_all_symbols_stream(callback=self.on_tick)
        else:
            Logger.log("Monitoring all symbols from local market data source")
            self.exchange.subscribe_to_local_datasource_ticker(callback=self.on_tick)