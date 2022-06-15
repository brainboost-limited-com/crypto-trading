
from decimal import Decimal as D, ROUND_DOWN, ROUND_UP
import abc
from datetime import datetime


from com_goldenthinker_trade_datatype.CryptoDict import CryptoDict
from com_goldenthinker_trade_datatype.CryptoFloat import CryptoFloat
import hashlib
import json

from com_goldenthinker_trade_model.Symbol import Symbol

class Order(metaclass=abc.ABCMeta):
    
    
    
    def __init__(self, quote_amt=None,base_qty=None,from_dict_value=None,parent_order=None,profit=None ):
        self.d = {}
        if from_dict_value is not None:
            self.d = from_dict_value
        else:
            if quote_amt is None and base_qty is not None:
                self.d['quote_amt'] = base_qty.get_symbol().as_quote_amt(base_qty)
                self.d['base_qty'] = base_qty
            else:
                if quote_amt is not None and base_qty is None:
                    self.d['base_qty'] = quote_amt.get_symbol().as_base_qty(quote_amt)
                    self.d['quote_amt'] = quote_amt
                else:
                    raise Exception('Order could not be created: Either quote_amt xor base_qty have to be set.')

            self.d['symbol'] = self.d['quote_amt'].get_symbol()
            
            self.d['timestampt'] = datetime.now()
            self.d['child'] = []
            self.d['parent_order'] = parent_order
            
            self.d['status'] = 'OPEN'
            self.d['dict_representation'] = None
            if profit != None:
                self.d['profit'] = profit
            


            from com_goldenthinker_trade_exchange.ExchangeConfiguration import ExchangeConfiguration
            self.exchange = ExchangeConfiguration.get_default_exchange()
            #self.d = self.to_dict()
            
        


    def execute_bfs(self):
        for child in self.child_orders:
            child.execute()
        self.execute()


    def execute_dfs(self):
        self.execute()
        for child in self.child_orders:
            child.execute()
    
    
    @abc.abstractmethod
    def execute(self):
        pass
    
    
    def get_crypto_float(self):
        return self.crypto_float
    
    def get_current_price(self):
        return self.get_symbol().get_current_price()
    
    def to_dict(self):
        if self.get_base_qty() is None:
            self.set_base_qty(float(CryptoFloat.get_neutral_element(self.get_symbol())))
        if self.get_quote_amt() is None:
            self.set_quote_amt(float(CryptoFloat.get_neutral_element(self.get_symbol())))
        
        self.set_base_qty(float(self.get_base_qty()))
        self.set_quote_amt(float(self.get_quote_amt()))
        self.set_symbol(self.get_symbol())
        from com_goldenthinker_trade_model.Symbol import Symbol
        self.set_price(float(Symbol(self.get_symbol()).get_current_price()))
        self.set_timestampt(str(datetime.now()))
        self.set_type(self.get_order_type())
        self.set_side(self.get_order_side())
        from com_goldenthinker_trade_exchange.ExchangeConfiguration import ExchangeConfiguration
        self.set_exchange(ExchangeConfiguration.get_default_exchange_name())
        self.set_status(self.get_status())
        self.set_profit(float(self.get_profit().get_value()))
        self.set_hash_id(self.generate_hash_id())
        self.set_child([x.to_dict() for x in self.d['child']])
        if self.d['parent_order']!=None:
            self.set_parent(self.d['parent_order'].generate_hash_id())
        else:
            self.set_parent(None)
        self.dict_representation = self.d
        return self.dict_representation
        

    def set_symbol(self,s):
        if type(s)==Symbol:
            self.d['symbol'] = s.uppercase_format()
        else:
            self.d['symbol'] = s

    def add_child_order(self,order):
        order.set_parent(self.generate_hash_id())
        self.get_child().append(order)
    
    def generate_hash_id(self):
        return (hashlib.sha1(json.dumps(self.d, sort_keys=True).encode()).hexdigest())[0:20]
    
    def set_parent(self,my_parent_order):
        self.d['parent_order'] = my_parent_order
        self.d['dict_representation']['parent_id'] = my_parent_order.generate_hash_id()
    
    def set_status_open(self):
        self.d['status'] = 'OPEN'
        
    def set_status_close(self):
        self.d['status'] = 'CLOSED'
        
    def set_timestampt(self,v):
        self.d['timestampt'] = v
        
    def set_exchange(self,v):
        self.d['exchange'] = v
               
    def set_type(self,v):
        self.d['type'] = v
        
    def set_profit(self,v):
        self.d['profit'] = v
        
    def get_profit(self):
        return self.d['profit']
        
    def set_side(self,v):
        self.d['side'] = v

    def set_status(self,v):
        self.d['status'] = v
               
    def set_hash_id(self,v):
        self.d['hash_id'] = v
        
    def set_child(self,v):
        self.d['child'] = v
        
    def set_parent(self,v):
        self.d['parent'] = v
        
    def get_status(self):
        return self.d['status']
    
    def set_price(self,v):
        if type(v)==Symbol:
            self.d['price'].get_current_price()
        else:
            self.d['price'] = v
    
    def save(self):
        from com_goldenthinker_trade_database.MongoConnector import MongoConnector
        o = MongoConnector.get_instance().find_order(self.generate_hash_id())
        if o == None:
            MongoConnector.get_instance().insert_order(self.to_dict())
        else:
            MongoConnector.get_instance().delete_order(self)
            MongoConnector.get_instance().insert_order(self.to_dict())
        
    def get_quote_amt(self):
        try:
            s = self.get_symbol()
        except:
            return None
        return CryptoFloat(s,float_value=self.d['quote_amt'])
    
    def set_quote_amt(self,amt):
        self.d['quote_amt'] = amt
        
    def get_base_qty(self):
        try:
            s = self.get_symbol()
        except:
            return None
        return CryptoFloat(s,float_value=self.d['base_qty']) 
    
    def set_base_qty(self,q):
        self.d['base_qty'] = q
    
    def get_symbol(self):
        try:
            return self.d['symbol']
        except:
            return None
        
    def get_symbol_str(self):    
        try:
            return self.d['symbol'].uppercase_format()
        except:
            return None
    
    def counter_order(self):
        pass
    
    @abc.abstractmethod
    def get_order_type(self):
        pass
        
    @abc.abstractmethod
    def get_order_side(self):
        pass
    
    def counter_order_partial(self,percentage):
        pass