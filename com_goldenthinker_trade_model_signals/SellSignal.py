from com_goldenthinker_trade_model_signals.Signal import Signal

from com_goldenthinker_trade_model_signals.Signal import Signal
from com_goldenthinker_trade_model_order.SellMarketOrder import SellMarketOrder
from com_goldenthinker_trade_scheduler.OrderScheduler import OrderScheduler
from com_goldenthinker_trade_utils.Date import Date
from com_goldenthinker_trade_datatype.CryptoFloat import CryptoFloat

class SellSignal(Signal):
    
    
    def __init__(self, signal_dict, when_signal_ocurred, channel_name):
        super().__init__(signal_dict=signal_dict, when_signal_ocurred=when_signal_ocurred, channel_name=channel_name)
    
    
    def valid(self):
        return self.has_symbol() and (not self.has_buy() and self.has_sell())
    
    
    def execute(self):
        o = SellMarketOrder(self)
        OrderScheduler.get_instance().schedule_sell(o)
        return True
    
    def is_worth_to_execute(self):
        pass
    
    
    def profit(self):
        pass
    
    
    def execute(self):
        pass

    
    def profit_forecast(self,signal):
        if Date().now() > self.get_timestampt():
            print("forecast")
        else:
            print("Forecasting is for the future only")

    
    def get_buy(self):
        return self.signal['buy']
    
    
    def get_sell(self):
        return None
    
    
    def get_stop(self):
        return CryptoFloat(self.get_symbol(),self.signal['stoploss']['numbers'][0])
    
    
    def has_symbol(self):
        return (self.get_symbol()!=None)
    
    
    def has_buy(self):
        return False
    
    def get_buy_price(self):
        return None
    
    def has_sell(self):
        return True
        
    def get_sell_price(self):
        return CryptoFloat(self.get_symbol(),self.signal['sell']['numbers'][0])
    
    def has_stop_loss(self):
        return self.get_stop().is_neutral_element()
    
    
    def calculate_profit(self):
        if Date().now() > self.get_timestampt():
            print("forecast")
        else:
            print("Forecasting is for the future only")
    
    
    def calculate_loss(self):
        if Date().now() > self.get_timestampt():
            print("forecast")
        else:
            print("Forecasting is for the future only")
    
    
    
    def valid(self):
        return self.get_symbol()!=None and self.get_sell()!=None and self.get_sell_price()!=None
