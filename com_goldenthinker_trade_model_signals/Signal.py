import sys
import abc
from com_goldenthinker_trade_datatype.CryptoFloat import CryptoFloat
from com_goldenthinker_trade_model.Symbol import Symbol
from com_goldenthinker_trade_utils.Date import Date
if 'com_goldenthinker_trade_database.TinyDbConnector' not in sys.modules:
    import com_goldenthinker_trade_database.TinyDbConnector
from com_goldenthinker_trade_exchange.ExchangeConfiguration import ExchangeConfiguration


class Signal(metaclass=abc.ABCMeta):

    def __init__(self,signal_dict=None,when_signal_ocurred=None,channel_name=None):
        if signal_dict!=None:
            self.signal = signal_dict
        self.signal['timestampt'] = when_signal_ocurred
        self.signal['channel'] = channel_name
        self.signal['id'] = self.generate_id()
        self.exchange = ExchangeConfiguration.get_default_exchange()
        
        
    def generate_id(self):
        return hash(str(type(self))+str(self.get_symbol().lowercase_format_slashed()) + str(self.get_timestampt()))

    def __str__(self):
        return str(self.signal)
    
    def save(self):
        com_goldenthinker_trade_database.TinyDbConnector.TinyDbConnector.instance_for_signals().save_signal(self)
    
    def to_dict(self):
        return self.signal
    
    def get_timestampt(self):
        return self.signal['timestampt']
    
    
    @abc.abstractmethod
    def is_worth_to_execute(self):
        pass
    
    @abc.abstractmethod
    def profit(self):
        pass
    
    @abc.abstractmethod
    def execute(self):
        pass

    @abc.abstractmethod
    def profit_forecast(self,signal):
        pass

    @abc.abstractmethod
    def get_buy(self):
        pass
    
    @abc.abstractmethod
    def get_sell(self):
        pass
    
    @abc.abstractmethod
    def get_stop(self):
        pass
    
    @abc.abstractmethod
    def has_symbol(self):
        pass
    
    @abc.abstractmethod
    def has_buy(self):
        pass
    
    @abc.abstractmethod
    def get_buy_price(self):
        pass
    
    
    @abc.abstractmethod
    def has_sell(self):
        pass
        
    @abc.abstractmethod
    def has_stop_loss(self):
        pass
    
    @abc.abstractmethod
    def calculate_profit(self):
        pass
    
    @abc.abstractmethod
    def calculate_loss(self):
        pass
    
    @abc.abstractmethod
    def valid(self):
        pass
    
    def get_symbol(self):
        return Symbol(self.signal['symbol_a']+'/'+self.signal['symbol_b'])
    
    
    
    def to_array(self):
        self.valid()
        return self.signal_array
    
    

        # day = 0
        # while day <
        #     e = d.add_days(amount_of_days=0)
        