import abc
from numpy import mean
from com_goldenthinker_trade_database.MongoConnector import MongoConnector


class Sequence(metaclass=abc.ABCMeta):
    
    def __init__(self,monitor=None,first_tick=None,next_sequence=None,previous_sequence=None):
        self.ticks = []
        self.next_sequence = next_sequence
        self.previous_sequence = previous_sequence
        self.monitor = monitor
        self.rise_drop_avg = MongoConnector.get_instance().average_drop_rise(self.monitor.get_symbol())
        self.rise_avg = self.rise_drop_avg[0]
        self.drop_avg = self.rise_drop_avg[1]
        self.rise_avg_delta_sum = self.rise_drop_avg[2]
        self.drop_avg_delta_sum = self.rise_drop_avg[3]
        
        
        if first_tick is not None:
            self.ticks.append(first_tick)
        
    @abc.abstractmethod
    def add_tick(self,tick):
        pass
        
    
    def next(self,next=None):
        if next is None:
            return self.next_sequence
        else:
            self.next_sequence = next
            return None
    
    def prev(self,prev=None):
        if prev is None:
            return self.previous_sequence
        else:
            self.previous_sequence = prev
            return None
        
        
    @abc.abstractmethod
    def __str__(self):
        pass
        
    
    
    def last_tick(self):
        if len(self.ticks) > 0:
            return self.ticks[len(self.ticks)-1]
        else:
            return None
    
    
    def sequence_time_lenght(self):
        if (len(self.ticks)>0):
            first_tick = self.ticks[0].get_timestampt()
            last_tick = self.ticks[len(self.ticks)-1]
            return (last_tick - first_tick)
        else:
            return 0
        

    @abc.abstractmethod    
    def analyze(self):
        pass

    def get_symbol(self):
        return self.monitor.get_symbol()