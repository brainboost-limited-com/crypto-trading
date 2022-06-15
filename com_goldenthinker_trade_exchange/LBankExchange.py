from com_goldenthinker_trade_exchange.Exchange import Exchange
from com_goldenthinker_trade_model.Symbol import Symbol
import cbpro
import time

class LBankExchange(Exchange):
    
    _instance = None
    
    @classmethod
    def instance(cls):
        if cls._instance == None:
            cls._instance = cls.__new__(cls)
        return cls._instance

    def __init__(self):
       
    
     
    def get_klines(self,symbol,date_a,date_b):
        getKline(symbol=symbol, size=, type='', time='')

    def get_current_price(self,symbol_uppercase):
        getTicker(symbol='')
    
    
    def balance(self,symbol):
        pass

    
    
    def portfolio(self):
        pass
    
    def get_list_of_symbols(self):
        getcurrencyPairs()


    
    
    def get_all_orders(self,symbol_uppercase):
§       getOpenOrder(symbol='',current_page=,page_length=)

    
    
    def get_symbol_information(self,symbol_str):
        getAccuracyInfo()

    
    
    def futures_create_order(self,symbol=None, side=None, type=None, quantity=None):
        createOrders(symbol='',type='',price=,amount=,customer_id='')
    
    
    def create_limit_buy_order(self,symbol,qty,price):
        createOrders(symbol='',type='',price=,amount=,customer_id='')
    
    
    def create_market_limit_order(self,symbol,qty):
        createOrders(symbol='',type='',price=,amount=,customer_id='')
    
    
    def create_limit_sell_order(self,symbol,qty,price):
        createOrders(symbol='',type='',price=,amount=,customer_id='')
    
    
    def order_market_buy(self,symbol_str_uppercase,float_quantity):
        createOrders(symbol='',type='',price=,amount=,customer_id='')
    
    
    def order_market_sell(self,symbol_str_uppercase,float_quantity):
        createOrders(symbol='',type='',price=,amount=,customer_id='')
    
    
    def get_all_tickers(self):
        getTicker(symbol='')
    
    def subscribe_multiple_individual_symbols(self,callback=None,symbols=[]):
        
     
            
    
    def subscribe_all_symbols_stream(self,callback=None):
§
    
    
    def subscribe(self,callback=None,symbols=[]):
        pass