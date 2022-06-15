
from com_goldenthinker_trade_datatype.DifferentSymbolsCrypto import DifferentSymbolsCrypto

from binance.helpers import round_step_size
import json


class CryptoFloat():


    
    @classmethod
    def get_neutral_element(cls,symbol):
        return CryptoFloat(symbol=symbol,float_value=0)



    # exchange is for including the fees in the float datatype
    def __init__(self,symbol,float_value: float):
        if (type(symbol)==str):
            from com_goldenthinker_trade_model.Symbol import Symbol
            self.symbol = Symbol(symbol)   # format :  eth/btc
        else:
            self.symbol = symbol
        self.float_value = float(float_value)
        
                
    
    def val(self):
        return float(self.float_value)
    
    def get_value(self):
        return float(self.float_value)
    
    
    def __radd__(self, other):
        if other == 0 or other == 0.0:
            return self
        else:
            return self.__add__(other)
    
    
    def __add__(self, another_crypto_float):
        if self.symbol!=another_crypto_float.symbol:
            raise DifferentSymbolsCrypto
        else:
            return CryptoFloat(self.symbol,self.float_value + another_crypto_float.float_value)
    
    def __sub__(self, another_crypto_float):
        if self.symbol!=another_crypto_float.symbol:
            raise DifferentSymbolsCrypto
        else:
            return CryptoFloat(self.symbol,self.float_value - another_crypto_float.float_value)
        
    def __div__(self,another_crypto_float):
        if type(another_crypto_float)!=CryptoFloat:
            if self.symbol!=another_crypto_float.symbol:
                raise DifferentSymbolsCrypto
            else:
                return CryptoFloat(self.symbol,self.float_value / another_crypto_float.float_value)   
        else:
            return CryptoFloat(self.symbol,(float(self.float_value)/float(another_crypto_float)))
        
    def __truediv__(self,another_crypto_float):
        if type(another_crypto_float)==CryptoFloat:
            if self.symbol!=another_crypto_float.symbol:
                raise DifferentSymbolsCrypto
            else:
                return CryptoFloat(self.symbol,self.float_value / another_crypto_float.float_value)
        else:
            return CryptoFloat(self.symbol,(float(self.float_value)/float(another_crypto_float)))
        
    def __mul__(self,another_crypto_float):
        if self.symbol!=another_crypto_float.symbol:
            raise DifferentSymbolsCrypto
        else:
            return CryptoFloat(self.symbol,self.float_value * another_crypto_float.float_value)
    
    def division(self,another_crypto_float):
        if self.symbol!=another_crypto_float.symbol:
            raise DifferentSymbolsCrypto
        else:
            return CryptoFloat(self.symbol,self.float_value / another_crypto_float.float_value)
        
    def __eq__(self, another_crypto_float):
        if not another_crypto_float is None:
            return (self.symbol==another_crypto_float.symbol) and (str(self)==str(another_crypto_float))
        else:
            return False
    
    def __gt__(self,another_crypto_float):
        if not another_crypto_float is None:
            return (self.symbol==another_crypto_float.symbol) and (self.float_value > another_crypto_float.float_value)
        else:
            return False
    
    def __lt__(self,another_crypto_float):
        if not another_crypto_float is None:
            return (self.symbol==another_crypto_float.symbol) and (self.float_value > another_crypto_float.float_value)
        else:
            return False
    
    def __ge__(self,another_crypto_float):
        if not another_crypto_float is None:
            return self.__gt__(another_crypto_float) or self.__eq__(another_crypto_float)
        else:
            return False
    
    def __le__(self,another_crypto_float):
        if not another_crypto_float is None:
            return self.__lt__(another_crypto_float) or self.__eq__(another_crypto_float)
        else:
            return False
    
    def step_up(self):
        return (self + CryptoFloat(self.symbol,self.step_size))
    
    def step_down(self):
        return (self - CryptoFloat(self.symbol,self.step_size))

    def __in__(self,crypto_range):
        if crypto_range.b != None:
            return (self >= crypto_range.a) and (self <= crypto_range.b) 
        else:
            return (self >= crypto_range.a)
        
    def __float__(self):
        return self.float_value
        
    def percent(self,x):
        return CryptoFloat(self.get_symbol().symbol_str,self.float_value*(x/100))

    
    def is_neutral_element(self):
        return self.float_value==0
    
    def get_float_as_string(self):
        return str(self.float_value)
    
    def to_usdt(self):
        if self.get_symbol().get_symbol_quote_asset().upper()=='USDT':
            return self
        else:
            val_one_base_in_usdt = self.get_symbol().to_usdt()
            return (val_one_base_in_usdt*CryptoFloat(symbol=val_one_base_in_usdt.get_symbol(),float_value=self.get_value()))
    
    def get_symbol(self):
        return self.symbol
    
    def get_current_quote(self):
        return self.get_symbol().get_current_price()
        
    
    def get_quote_value(self):
        return self.get_value()
    
    
    def get_rounded_base_quantity(self):
        return round_step_size((float(self.get_quote_value())/float(self.get_symbol().get_current_price())), float(self.get_symbol().get_step_size()))
    
    def toJson(self):
        return json.dumps(self, default=lambda o: o.__dict__)
    
    
    def __str__(self) -> str:
        return "<" + self.get_symbol().uppercase_format() + "_" + self.get_float_as_string() + ">"
    
