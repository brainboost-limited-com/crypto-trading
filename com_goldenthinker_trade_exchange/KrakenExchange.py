from com_goldenthinker_trade_exchange.Exchange import Exchange
#from com_goldenthinker_trade_exchange.ExchangeConfiguration import ExchangeConfiguration
from com_goldenthinker_trade_model.Symbol import Symbol
import cbpro
import time
#import krakenex

class KrakenExchange(Exchange):
    
    _instance = None
    
    @classmethod
    def instance(cls):
        if cls._instance == None:
            cls._instance = cls.__new__(cls)
        return cls._instance

    def __init__(self):
        self.public_client = krakenex.API()
       # self.auth_client = self.public_client.load_key(ExchangeConfiguration.get_exchange_by_name(name='kraken'))

    
     
    def get_klines(self,symbol,date_a,date_b):
        return self.public_client.get_product_historic_rates(symbol.uppercase_dash_format(), granularity=3000)
    
    def get_current_price(self,symbol_uppercase):
        s = Symbol(symbol_uppercase).uppercase_dash_format()
        return self.public_client.get_product_ticker(product_id=s)
    
    
    def balance(self,symbol):
        
        balance = self.public_client.query_private('Balance')
            
        return balance
    
    
    def portfolio(self):
        return self.auth_client.get_accounts()
    
    
    def get_list_of_symbols(self):
        return self.public_client.get_currencies()

    
    
    def get_all_orders(self,symbol_uppercase):
        return self.public_client.get_product_trades(product_id=symbol_uppercase)

    
    
    def get_symbol_information(self,symbol_str):
        pass
    
    
    def futures_create_order(self,symbol=None, side=None, type=None, quantity=None):
        pass
    
    
    def create_limit_buy_order(self,symbol,qty,price):
        pass
    
    
    def create_market_limit_order(self,symbol,qty):
        pass
    
    
    def create_limit_sell_order(self,symbol,qty,price):
        pass
    
    
    def order_market_buy(self,symbol_str_uppercase,float_quantity):
        pass
    
    
    def order_market_sell(self,symbol_str_uppercase,float_quantity):
        pass
    
    
    def get_all_tickers(self):
        all_symbols = [Symbol(x.replace('-','/')) for x in self.get_list_of_symbols()]
        tickers = dict()
        for s in all_symbols:
            tickers[s.uppercase_dash_format()] = self.public_client.get_product_ticker(product_id=s.uppercase_dash_format())
        return tickers
            
            
            
    
    def subscribe_multiple_individual_symbols(self,callback=None,symbols=[]):
        
        class myWebsocketClient(cbpro.WebsocketClient):
            def on_open(self):
                self.url = "wss://ws-feed.pro.Kraken.com/"
                self.products = [x.uppercase_dash_format() for x in symbols]
                self.message_count = 0
                print("Lets count the messages!")
                
                
            def on_message(self, msg):
                
                def callback_example():
                    if 'price' in msg and 'type' in msg:
                        print ("Message type:", msg["type"],
                        "\t@ {:.3f}".format(float(msg["price"])))
                
                
                callback = callback_example
                self.message_count += 1
                callback()
                
            
            
            def on_close(self):
                print("-- Goodbye! --")
        
        wsClient = myWebsocketClient()
        wsClient.start()
        print(wsClient.url, wsClient.products)
        while (wsClient.message_count < 500):
            print ("\nmessage_count =", "{} \n".format(wsClient.message_count))
            time.sleep(1)
        
            
            
    
    def subscribe_all_symbols_stream(self,callback=None):
        all_symbols = [Symbol(x.replace('-','/')) for x in self.get_list_of_symbols()]
        self.subscribe_multiple_individual_symbols(symbols=all_symbols)
        
    
    
    def subscribe(self,callback=None,symbols=[]):
        pass