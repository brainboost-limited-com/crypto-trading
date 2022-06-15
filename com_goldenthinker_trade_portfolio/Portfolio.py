from com_goldenthinker_trade_config.Config import Config
from com_goldenthinker_trade_datatype.CryptoDict import CryptoDict
from com_goldenthinker_trade_datatype.CryptoFloat import CryptoFloat
from com_goldenthinker_trade_exchange.ExchangeConfiguration import ExchangeConfiguration
from com_goldenthinker_trade_database.MongoConnector import MongoConnector
from com_goldenthinker_trade_exchange.SandboxExchange import SandboxExchange
from com_goldenthinker_trade_logger.Logger import Logger
from com_goldenthinker_trade_model.Symbol import Symbol
from com_goldenthinker_trade_model_order.BuyMarketOrder import BuyMarketOrder
from com_goldenthinker_trade_model_order.OrderFactory import OrderFactory
from com_goldenthinker_trade_model_order.SellMarketOrder import SellMarketOrder
from com_goldenthinker_trade_config.Config import Config
import itertools


class Portfolio:
    
    _portfolio = None


    @classmethod
    def instance(cls,sandbox=True,initial_balance=None):
        if cls._portfolio is None:
            cls._portfolio = Portfolio(sandbox=sandbox,initial_balance=initial_balance)
        return cls._portfolio
    
    
    def __init__(self,sandbox=True,initial_balance=None):

        self.exchange = ExchangeConfiguration.get_default_exchange()

        self.portfolio_dict = self.exchange.portfolio()
        self.portfolio_currencies = [k.upper() for k in list(self.portfolio_dict.keys())]   
        self.ongoing_orders_cache = None

    def generate_sell_order(self,amount):
        so = SellMarketOrder(amount)
        so.execute()


    def get_portfolio_currencies(self):
        return self.portfolio_currencies

    
    def get_asset_balance(self,symbol):
        return self.portfolio_dict[symbol]

    
    def get_portfolio(self):
        return self.portfolio_dict


    def get_orders(self):
        if not Config.sandbox():
            if self.ongoing_orders_cache==None:
                assets = self.get_portfolio_currencies()
                symbols = ExchangeConfiguration.get_default_exchange().get_list_of_symbols()
                symbols_uppercase = [ Symbol(s).uppercase_format() for s in symbols]
                possible_symbols_that_have_ongoing_orders = [s for s in symbols_uppercase if any((s.find(s1)==0) for s1 in assets)]
                ongoing_orders = [x for x in [ExchangeConfiguration.get_default_exchange().get_all_orders(o) for o in possible_symbols_that_have_ongoing_orders] if x != []]
                self.ongoing_orders_cache = ongoing_orders
            else:
                ongoing_orders = self.ongoing_orders_cache
        else:
            ongoing_orders = SandboxExchange.get_all_orders()
        return ongoing_orders


    def get_currencies_in_orders(self):
        orders = self.get_orders()
        return list(set([x.get_symbol() for x in orders]))



    
    # The min amount is never touched so in order to generate an order needs the min a 
        
        
    def generate_buy_order(self,symbol):
        try:
            existing_orders_for_symbol = self.exchange.get_all_orders(symbol)
            min_amount = float(symbol.get_min_notional())
            symbol_balance = float(self.portfolio_dict[symbol.get_symbol_quote_asset().lower()])
            stats_to_generate_reasonable_invest_amounts = MongoConnector.get_instance().drop_rise_stats(symbol=symbol)    #Check if not none
            if stats_to_generate_reasonable_invest_amounts is not None:
                money_to_use = symbol_balance - (min_amount*2)   # we always leave a minimum balance
                
                if money_to_use < (min_amount*2):
                    Logger.log("Order should be higher than the mim amount * of " + str(min_amount) + " " + symbol.uppercase_format())
                else:
                    #if len(existing_orders_for_symbol)==0:     # Generate orders if there are not ongoing existing orders for the same symbol
                    if symbol_balance < (min_amount*2):
                        Logger.log("Balance is a bit low, less than twice the min_notional.")
                    else:
                        current_quote_per_one_base = symbol.get_current_price().float_value
                        am = current_quote_per_one_base * ((int(symbol.balance().float_value/current_quote_per_one_base))-1)

                        # THe variable stats_to_generate_reasonable_invest_amounts has statistics that are useful when the
                        # order is being monitored in real time as with this will sell when it is expected to drop
                        am_1 = CryptoFloat(symbol=symbol,float_value=am)
                        o = OrderFactory.get_instance().generate_buy_order_from_analysis(amount_in_crypto_float=am_1,analysis=stats_to_generate_reasonable_invest_amounts)

                        return o
            else:
                return None
        except:
            return None
                    

                    
                  