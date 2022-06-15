
from datetime import datetime, timedelta
from com_goldenthinker_trade_datasource.PeriodicDataSource import PeriodicDataSource
from com_goldenthinker_trade_datainput.DataInputManager import DataInputManager
from com_goldenthinker_trade_database.MongoConnector import MongoConnector
from com_goldenthinker_trade_exchange.ExchangeConfiguration import ExchangeConfiguration
import time

class LastMinuteSymbolStreamDataSource(PeriodicDataSource):
    
    def __init__(self,name=None,minutes_ago=30,listener=None):
        super().__init__(name=name,minutes_ago=minutes_ago)
        if listener!=None:
            self.subscribe(listener=listener)
        

        
    def start(self):
        DataInputManager.get_input('logger').input("Last " + str(self.minutes_ago) + " minutes sequence activity per symbol.")
        while True:
            current = datetime.now()
            data = MongoConnector.get_instance().get_all_data_in_the_last_minutes_for_all_symbols(ExchangeConfiguration.get_default_exchange_name(),self.minutes_ago)
            after_query = datetime.now()
            time_query_took = after_query-current
            for l in self.listeners:
                l.notify(data)
            if (time_query_took<timedelta(minutes=self.minutes_ago)): 
                wait_time = timedelta(minutes=self.minutes_ago).total_seconds()-time_query_took.total_seconds()
                DataInputManager.get_input('logger').input("Obtained last minutes sequences successfully, now waiting " + str(wait_time))
                print("finished..")
                time.sleep(wait_time)
                print("Executing again")
            
            
                