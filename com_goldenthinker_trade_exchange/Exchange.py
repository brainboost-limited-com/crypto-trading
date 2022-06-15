from abc import abstractclassmethod, abstractmethod


class Exchange:
    
    @abstractclassmethod
    def instance():
        pass
    
    @abstractmethod
    def get_klines(self,symbol,date_a,date_b):
        pass
    
    @abstractmethod
    def balance(self,symbol):
        pass
    
    @abstractmethod
    def get_current_price(self,symbol_uppercase):
        pass
    
    @abstractmethod
    def balance(self,symbol):
        pass
    
    @abstractmethod
    def portfolio(self):
        pass
    
    @abstractmethod
    def get_list_of_symbols(self):
        pass
    
    @abstractmethod
    def get_all_orders(self,symbol_uppercase):
        pass
    
    @abstractmethod
    def get_symbol_information(self,symbol_str):
        pass
    
    @abstractmethod
    def futures_create_order(self,symbol=None, side=None, type=None, quantity=None):
        pass
    
    @abstractmethod
    def create_limit_buy_order(self,symbol,qty,price):
        pass
    
    @abstractmethod
    def create_market_limit_order(self,symbol,qty):
        pass
    
    @abstractmethod
    def create_limit_sell_order(self,symbol,qty,price):
        pass
    
    @abstractmethod
    def order_market_buy(self,symbol_str_uppercase,float_quantity):
        pass
    
    @abstractmethod
    def order_market_sell(self,symbol_str_uppercase,float_quantity):
        pass
    
    @abstractmethod
    def get_all_tickers(self):
        pass
    
    
    @abstractmethod
    def subscribe(self,callback=None,symbols=[]):
        pass