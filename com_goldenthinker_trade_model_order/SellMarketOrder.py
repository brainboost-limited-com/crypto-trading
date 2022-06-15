from datetime import datetime
from binance.helpers import round_step_size
from com_goldenthinker_trade_logger.Logger import Logger



from com_goldenthinker_trade_datatype.CryptoFloat import CryptoFloat
from com_goldenthinker_trade_scheduler.OrderScheduler import OrderScheduler


from com_goldenthinker_trade_model_order.Order import Order


class SellMarketOrder(Order):
    
    def __init__(self, base_qty=None, quote_amt=None,from_dict_value=None,parent_order=None,profit=None):
        super().__init__(base_qty=base_qty,quote_amt=quote_amt,from_dict_value=from_dict_value,parent_order=parent_order,profit=profit)
        


    
    def execute(self):
        from com_goldenthinker_trade_exchange.ExchangeConfiguration import ExchangeConfiguration
        exchange = ExchangeConfiguration.get_default_exchange()
        exchange.order_market_sell(self)
        from com_goldenthinker_trade_model.Symbol import Symbol
        orders_in_exchange = exchange.get_all_orders(Symbol(self.get_symbol()))
        if len(orders_in_exchange) > 0:
            Logger.log('Order placed ' + str(self.get_symbol()) + ' ' + str(self.get_quote_amt().get_rounded_base_quantity()) + " balance " + str(Symbol(self.get_symbol()).balance()),telegram=True)
            #self.order_id = 
            return True
        else:
            Logger.log('Error placing sell market order in exchange'  + self.get_symbol().uppercase_format(),telegram=True)
            return False
    

  
  
    def get_order_type(self):
        return 'MARKET'
        
    def get_order_side(self):
        return 'SELL'  
    
    def counter_order(self):
        from com_goldenthinker_trade_model_order.BuyMarketOrder import BuyMarketOrder
        return BuyMarketOrder(base_qty=self.get_base_qty(),quote_amt=self.get_quote_amt())
 

    def counter_order_partial(self,percentage: float):
        from com_goldenthinker_trade_model_order.BuyMarketOrder import BuyMarketOrder
        partial_amount = self.get_base_qty().percent(percentage)
        counter_order = BuyMarketOrder(base_qty=partial_amount,profit=self.get_profit(),parent_order=self)
        counter_order.add_child_order(self)
        return counter_order
    