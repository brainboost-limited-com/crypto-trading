from com_goldenthinker_trade_model_order.Order import Order
from com_goldenthinker_trade_logger.Logger import Logger

class FuturesBuyMarketOrder(Order):
    
    def __init__(self, base_qty=None, quote_amt=None):
        super().__init__(base_qty=base_qty,quote_amt=quote_amt )
        
        
    def execute(self):
        pass
    
    def get_order_type(self):
        return 'MARKET'
    
    def get_order_side(self):
        return 'BUY'
    