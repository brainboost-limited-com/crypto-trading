from com_goldenthinker_trade_datasource.LastMinuteSymbolStreamDataSource import LastMinuteSymbolStreamDataSource
from com_goldenthinker_trade_datasource.DataSourceManager import DataSourceManager
from com_goldenthinker_trader_robot.Robot import Robot
from decimal import Decimal



from com_goldenthinker_trade_strategy.Strategy import Strategy
from com_goldenthinker_trade_datasource.RealTimeDataSource import RealTimeDataSource

# Receives input notifications and acts upon processing the data
# and returns the new data



class StrategyRealTimeDataSource(RealTimeDataSource):
    
    def __init__(self, name, trust=Decimal(0.999999), session=None):
        super().__init__(name, trust, session)

        
        self.last_min_sequences_all_symbols = DataSourceManager.get_data_source('last_min_sequences_all_symbols')
        self.last_min_sequences_all_symbols.subscribe(self)
        self.last_min_sequences_all_symbols.start()

        
    def notify(self,data):
        super().notify(data)
        self.strategy = Strategy(data=data)
        average_sequence_per_symbol = self.strategy.for_each_symbol_calculate_sequence_average_in_the_last_minutes()
        
        
        
    def start(self):
        super().start()
        
        
        
        
        return True