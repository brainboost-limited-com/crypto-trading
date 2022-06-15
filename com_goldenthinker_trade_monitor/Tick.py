import datetime
from com_goldenthinker_trade_datatype.CryptoFloat import CryptoFloat


class Tick:


    def __init__(self, data):
        self.value = data['c']
        self.data = data
        self.timestampt = datetime.datetime.utcnow()
        self.last_tick = None
        self.e = data['e']
        self.E = data['E']
        self.s = data['s']
        self.p = data['p']
        self.P = data['P']
        self.w = data['w']
        self.x = data['x']
        self.c = data['c']
        self.Q = data['Q']
        self.b = data['b']
        self.B = data['B']
        self.a = data['a']
        self.A = data['A']
        self.o = data['o']
        self.h = data['h']
        self.l = data['l']
        self.v = data['v']
        self.q = data['q']
        self.O = data['O']
        self.C = data['C']
        self.F = data['F']
        self.L = data['L']
        self.n = data['n']



    def set_event_type(self,val):
        self.e = val
    def set_event_time(self,val):    
        self.E = val
    def set_symbol(self,val):
        self.s = val
    def set_price_change(self,val):
        self.p = val
    def set_price_change_percent(self,val):
        self.P = val
    def set_weighted_average_price(self,val):
        self.w = val
    def set_first_trade(self,val):
        self.x = val
    def set_last_price(self,val):
        self.c = val
    def set_last_quantity(self,val):
        self.Q = val
    def set_best_bid_price(self,val):
        self.b = val
    def set_best_bid_quantity(self,val):
        self.B = val
    def set_best_ask_price(self,val):
        self.a = val
    def set_best_ask_quantity(self,val):
        self.A = val
    def set_open_price(self,val):
        self.o = val
    def set_high_price(self,val):
        self.h = val
    def set_low_price(self,val):
        self.l = val
    def set_total_traded_base_asset_volume(self,val):
        self.v = val
    def set_total_traded_quote_asset_volume(self,val):
        self.q = val
    def set_statistics_open_time(self,val):
        self.O = val
    def set_statistics_close_time(self,val):
        self.C = val
    def set_first_trade_id(self,val):
        self.F = val
    def set_last_trade_id(self,val):
        self.L = val
    def set_total_number_of_trades(self,val):
        self.n = val
        

        
    
    def get_event_type(self):
        return self.e
    def get_event_time(self):    
        return self.E
    def get_symbol(self):
        return self.s
    def get_price_change(self):
        return CryptoFloat(self.get_symbol(),float(self.p))
    def get_price_change_percent(self):
        return CryptoFloat(self.get_symbol(),float(self.P))
    def get_weighted_average_price(self):
        return CryptoFloat(self.get_symbol(),float(self.w))
    def get_first_trade(self):
        return CryptoFloat(self.get_symbol(),float(self.x))
    def get_last_price(self):
        return CryptoFloat(self.get_symbol(),float(self.c))
    def get_last_quantity(self):
        return CryptoFloat(self.get_symbol(),float(self.Q))
    def get_best_bid_price(self):
        return CryptoFloat(self.get_symbol(),float(self.b))
    def get_best_bid_quantity(self):
        return CryptoFloat(self.get_symbol(),float(self.B))
    def get_best_ask_price(self):
        return CryptoFloat(self.get_symbol(),float(self.a))    
    def get_best_ask_quantity(self):
        return CryptoFloat(self.get_symbol(),float(self.A))   
    def get_open_price(self):
        return CryptoFloat(self.get_symbol(),float(self.o))  
    def get_high_price(self):
        return CryptoFloat(self.get_symbol(),float(self.h)) 
    def get_low_price(self):
        return CryptoFloat(self.get_symbol(),float(self.l))
    def get_total_traded_base_asset_volume(self):
        return CryptoFloat(self.get_symbol(),float(self.v))
    def get_total_traded_quote_asset_volume(self):
        return CryptoFloat(self.get_symbol(), float(self.q))
    def get_statistics_open_time(self):
        return self.O
    def get_statistics_close_time(self):
        return self.C
    def get_first_trade_id(self):
        return self.F
    def get_last_trade_id(self):
        return self.L
    def get_total_number_of_trades(self):
        return self.n    
        

    def get_data(self):
        return self.data
        
    def get_value(self):
        return float(self.get_last_price())
    
    def set_value(self,val):
        self.set_last_price(val)
    
    
    def set_last_tick(self,last_tick):
        self.last_tick = last_tick
        
    def get_last_tick(self):
        return self.last_tick
    
    def get_delta(self):
        if self.get_last_tick() is not None:
            return float(self.get_value() - float(self.get_last_tick().get_value()))
        else:
            return float(0)
        
    def get_delta_time(self):
        if self.get_last_tick() is not None:
            return (self.get_timestampt() - self.get_last_tick().get_timestampt()).total_seconds()
        else:
            a = datetime.datetime.utcnow()
            b = a
            return (b-a).total_seconds()
    
    
    def get_timestampt(self):
        return (self.timestampt)
    
    def __gt__(self,another_tick):
        return self.get_value() > another_tick.get_value()
    
    def __lt__(self,another_tick):       # we treat equal ticks as dropping 
        if another_tick is not None:
            return self.get_value() <= another_tick.get_value()
        else:
            return True
    
    def __eq__(self,another_tick):
        if another_tick != None:
            return (self.value == another_tick.get_value()) and (self.get_timestampt() == another_tick.get_timestampt())
        else:
            return False
    
    def __str__(self):
        ret = dict()
        ret['value'] = self.get_value()
        ret['timestampt'] = self.get_timestampt()
        if self.get_last_tick() is None:
            ret['value_delta'] = self.get_value()
        else:
            ret['value_delta'] = (self.get_value() - self.get_last_tick().get_value())
            ret['time_delta'] = (self.get_timestampt() - self.get_last_tick().get_timestampt()).total_seconds()
        ret['data'] = self.get_data()
        return str(ret)
    
    def __repr__(self):
        return str(self)
    
    def __dict__(self):
        ret = dict()
        ret['value'] = self.get_value()
        ret['timestampt'] = self.get_timestampt()
        if self.get_last_tick() is None:
            ret['value_delta'] = self.get_value()
        else:
            ret['value_delta'] = (self.get_value() - self.get_last_tick().get_value())
            ret['time_delta'] = (self.get_timestampt() - self.get_last_tick().get_timestampt()).total_seconds()
        ret['data'] = self.get_data()
        return ret
        
    def to_dict(self):
        return self.__dict__()