from com_goldenthinker_trade_database.MongoConnector import MongoConnector
from com_goldenthinker_trade_monitor.DroppingSequence import DroppingSequence


class SymbolMonitor:
    
    
    def __init__(self,symbol):
        self.symbol = symbol
        self.first_sequence = DroppingSequence(monitor=self,previous_sequence=None,next_sequence=None)
        self.current_sequence = self.first_sequence
        self.last_tick = None
        self.ticks = []
        self.strategy = None
        self.delta_rise_max = 0
        self.delta_rise_min = 0
        self.delta_drop_max = 9999999999
        self.delta_drop_min = 9999999999
        self.delta_longest_time_rise = 9999999999
        self.delta_shorter_time_rise = 0
        self.delta_longest_time_drop = 0
        self.delta_shorter_time_drop = 9999999999

        
        
    def get_symbol(self):
        return self.symbol
    
    def tick(self,current_quote):
        #Logger.log("tick_thread_start," + str(self.get_symbol().uppercase_format_slashed()))
        tick = current_quote
        if self.last_tick is not None:
            tick.set_last_tick(self.last_tick)
        self.ticks.append(tick)
        self.last_tick = tick
        self.update_status(tick)
        #Logger.log("tick_thread_end," + str(self.get_symbol().uppercase_format_slashed()))
        
        
    def get_first_sequence(self):
        return self.first_sequence
    
    def set_first_sequence(self,seq):
        self.first_sequence = seq
        
    def set_current_sequence(self,seq):
        self.current_sequence = seq
    
    def get_current_sequence(self):
        return self.current_sequence
    
    def update_status(self,current_tick):
        if (len(self.ticks)==1):
            self.get_current_sequence().add_tick(current_tick)
        else:
            self.set_current_sequence(self.get_current_sequence().add_tick(current_tick))
        #Strategy(self).study_sequence(self.get_current_sequence())
            
    
    def print_all_sequences(self):
        iterseq = self.get_current_sequence()
        while iterseq.next() is not None:
            print(str(iterseq))
            iterseq = iterseq.next()
    
    def print_current_sequence(self):
        print(str(self.get_current_sequence()))
    
    def insert_sequence_to_db(self,sequence=None,symbol=None):
        #MongoConnector.get_instance().insert_sequence_into_new_document_or_push_to_existing(sequence=sequence,symbol=symbol)
        from com_goldenthinker_trade_exchange.ExchangeConfiguration import ExchangeConfiguration
        MongoConnector.get_instance().MongoConnector.get_instance().insert_sequence(sequence=sequence,symbol=symbol,exchange=ExchangeConfiguration.get_default_exchange_name())
        
    def get_symbol(self):
        return self.symbol