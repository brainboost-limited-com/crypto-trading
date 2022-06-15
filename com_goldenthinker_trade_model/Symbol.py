import time
from urllib3.exceptions import ProtocolError
from requests.exceptions import ChunkedEncodingError
from binance.helpers import round_step_size
import math
from com_goldenthinker_trade_config.Config import Config

from com_goldenthinker_trade_datatype.CryptoFloat import CryptoFloat

class Round:
    def step_size_to_precision(self, ss):
        return ss.find('1') - 1

    def format_value(self, val, step_size_str):
        precision = self.step_size_to_precision(step_size_str)
        if precision > 0:
            return "{:0.0{}f}".format(val, precision)
        return math.floor(int(val))

    def format_valueDown(self, val, step_size_str):
        precision = self.step_size_to_precision(step_size_str)
        if precision > 0:
            return "{:0.0{}f}".format(val, precision)
        return math.trunc(int(val)) 

class Symbol:
    
    # defualt format :  eth/btc
    def __init__(self,symbol_str):
        from com_goldenthinker_trade_exchange.ExchangeConfiguration import ExchangeConfiguration
        try:
            if (symbol_str.isupper()):
                self.symbol = symbol_str
                symbol_data = ExchangeConfiguration.get_default_exchange().get_symbol_information(self)
            else:
                self.symbol = symbol_str
                print('symbol is: ' + str(symbol_str))
                self.symbol_a = symbol_str.split('/')[0]
                self.symbol_b = symbol_str.split('/')[1]
                from com_goldenthinker_trade_model.Symbol import Symbol
                symbol_data = ExchangeConfiguration.get_default_exchange().get_symbol_information(Symbol(self.symbol_a+self.symbol_b))
            
            
            self.step = symbol_data['step']
            self.base_asset = symbol_data['baseAsset']
            self.quote_asset = symbol_data['quoteAsset']
            self.precision = symbol_data['precision']
            # filters
            
            self.min_notional = symbol_data['min_notional']
            self.min_quantity = symbol_data['min_quantity']
            self.max_quantity = symbol_data['max_quantity']
            #self.max_quantity_precision = symbol_data['']
            self.step_size = symbol_data['step_size']
            self.tick_size = symbol_data['tick_size']
            
            # precision
            self.base_asset_precision = symbol_data['base_asset_precision']
            self.quote_precision = symbol_data['quote_precision']
            self.quote_asset_precision = symbol_data['quote_asset_precision']
            self.base_comission_precision = symbol_data['base_comission_precision']
            self.quote_comission_precision = symbol_data['quote_comission_precision']
            if Config.sandbox is True:
                self.balance_sandbox = CryptoFloat(self.symbol,ExchangeConfiguration.get_default_exchange().balance(symbol=self))
    
        except ConnectionResetError:
            time.sleep(69)
            print("Connection Reset Error...")
        except ProtocolError:
            time.sleep(69)
            print("Connection Reset Error...")     
        except ConnectionError:
            time.sleep(60)
            print("Connection Error...")  
        except ChunkedEncodingError:
            time.sleep(60)
            print("ChunkedEncodingError...")
        
    def get_symbol_base_asset(self):
        return self.base_asset
    
    def get_symbol_quote_asset(self):
        return self.quote_asset
    
    def get_base_asset_precision(self):
        return self.base_asset_precision
    
    def get_quote_comission_precision(self):
        return self.quote_comission_precision
    
    def get_step_size(self):
        return float(self.step_size)
    
    def get_tick_size(self):
        return self.tick_size
    
    def get_min_notional(self):
        from com_goldenthinker_trade_datatype.CryptoFloat import CryptoFloat
        return CryptoFloat(self,float_value=self.min_notional)
    
    def uppercase_format(self) -> str:
        return self.symbol.replace('/','').upper()
    
    def lowercase_format(self) -> str:
        return self.symbol.replace('/','')
    
    def uppercase_dash_format(self) -> str:
        return self.symbol.replace('/','-').upper() 
    
    def uppercase_format_slashed(self) -> str:
        return self.symbol.upper()
    
    def lowercase_format_slashed(self):
        return self.symbol
    
    def __eq__(self,symbol):
        if symbol!=None:
            return (self.symbol == symbol.symbol)
        else:
            return False
        
    def __lt__(self,symbol):
        return self.to_usdt < symbol.to_usdt()
    
    def __gt__(self,symbol):
        return self.to_usdt > symbol.to_usdt()
    
    
    def as_base_qty(self,quote_amt: CryptoFloat):
        base_qty = quote_amt.division(self.get_current_price())
        return CryptoFloat(symbol=self,float_value=base_qty.get_value())
    
    def as_quote_amt(self,base_qty: CryptoFloat):
        quote_amt = base_qty.division(self.get_current_price())
        return CryptoFloat(symbol=self,float_value=quote_amt.get_value())
    
    
    def get_current_price(self):
        from com_goldenthinker_trade_exchange.ExchangeConfiguration import ExchangeConfiguration
        from com_goldenthinker_trade_datatype.CryptoFloat import CryptoFloat
        return CryptoFloat(self.symbol,ExchangeConfiguration.get_default_exchange().get_current_price(self))
    
    def balance(self):
        if Config.sandbox is True:
            return self.balance_sandbox
        else:
            from com_goldenthinker_trade_exchange.ExchangeConfiguration import ExchangeConfiguration
            from com_goldenthinker_trade_datatype.CryptoFloat import CryptoFloat
            return CryptoFloat(self.symbol,ExchangeConfiguration.get_default_exchange().balance(symbol=self))
        
    def decrease_sandbox_balance(self,amount):
        self.balance_sandbox = self.balance_sandbox - amount
    
    def max_quantity_i_can_buy(self):

        if (float(self.balance()) < float(self.max_quantity)):
            max_quantity_i_can_buy = float(float(self.balance())/float(self.get_current_price()))
        else:
            max_quantity_i_can_buy = float(0)
        from com_goldenthinker_trade_datatype.CryptoFloat import CryptoFloat
        return CryptoFloat(self.symbol, self.get_rounded_number(max_quantity_i_can_buy))
        
    def min_quantity_i_can_buy(self):
        if (float(self.balance()) > float(self.min_notional)):
            min_quantity_i_can_buy = float(float(self.min_notional)/float(self.get_current_price()))
        else:
            min_quantity_i_can_buy = float(0)
        from com_goldenthinker_trade_datatype.CryptoFloat import CryptoFloat
        return CryptoFloat(self.symbol,self.get_rounded_number(min_quantity_i_can_buy))
    
    def max_amount_i_can_spend(self):
        from com_goldenthinker_trade_datatype.CryptoFloat import CryptoFloat
        return CryptoFloat(self.symbol,self.get_rounded_number(float(self.max_quantity_i_can_buy())*float(self.get_current_price())))
    
    def min_amount_i_can_spend(self):
        from com_goldenthinker_trade_datatype.CryptoFloat import CryptoFloat
        return CryptoFloat(self.symbol,self.get_rounded_number(float(self.min_quantity_i_can_buy())*float(self.get_current_price())))
    
    
    def percent_of_balance(self,percent):
        from com_goldenthinker_trade_datatype.CryptoFloat import CryptoFloat
        return (CryptoFloat(self.symbol,percent)/CryptoFloat(self.symbol,100))*CryptoFloat(self.symbol,self.balance().get_value())
        
    
    def what_percentage_is_another_number_of_myself(self,another_number):
        return CryptoFloat(self.symbol,another_number)/(self.get_current_price()*CryptoFloat(self.symbol,100))
    
    
    def closest_possible_value_to_base_quantity(self,hipotetical_qty):
        a = 0
        y = int(float(hipotetical_qty)/float(self.step_size))
        for i in range(0,y-1):
            a = a + float(self.step_size)
        from com_goldenthinker_trade_datatype.CryptoFloat import CryptoFloat
        return CryptoFloat(self.symbol,self.get_rounded_number(a*float(self.get_current_price())))
    
    
    def closest_possible_amount_to_amount(self,hipotetical_amount):
        a = 0
        y = int(float(hipotetical_amount)/float(self.step_size))
        for i in range(0,y-1):
            a = a + float(self.step_size)
        from com_goldenthinker_trade_datatype.CryptoFloat import CryptoFloat
        return CryptoFloat(self.symbol,self.get_rounded_number(float((self.get_current_price()))))
    
    def get_all_orders(self):
        from com_goldenthinker_trade_exchange.ExchangeConfiguration import ExchangeConfiguration
        return ExchangeConfiguration.get_default_exchange().get_all_orders(symbol=self)

    def to_usdt(self):
        if self.quote_asset.upper() != 'USDT':
            quote_in_usdt = Symbol(self.quote_asset+'USDT').get_current_price()
            return quote_in_usdt
        else:
            return self.get_current_price()

    
    
    def get_rounded_number(self,num):
        res = round_step_size(float(num), float(self.get_step_size()))
        #res1 = Round().format_value(num, self.get_step_size())
        return res
    
    def __str__(self) -> str:
        return self.uppercase_format()
    
