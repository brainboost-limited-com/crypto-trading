
from abc import abstractmethod
from com_goldenthinker_trade_datainput.DataInputManager import DataInputManager
from com_goldenthinker_trade_datasource.DataSource import DataSource
from datetime import timedelta

class PeriodicDataSource(DataSource):
    
    def __init__(self,name=None,minutes_ago=1):
        super().__init__(name)
        self.minutes_ago = minutes_ago
        self.listeners = []
        self.name = name
        
        
    
    def subscribe(self,listener):
        self.listeners.append(listener)
    
    @abstractmethod
    def start(self):
        pass
        