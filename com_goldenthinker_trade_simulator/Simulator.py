
from com_goldenthinker_trade_logger.Logger import Logger


class Simulator:
    
    _instance = None
    _orders = {}
    
    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = Simulator()
        return cls._instance
    
    def __init__(self):
        pass
    
    
    def buy(self,order_buy):
        from com_goldenthinker_trade_model.Symbol import Symbol
        s = Symbol(order_buy.get_symbol())
        Simulator._orders[s.uppercase_format()] = order_buy
        from com_goldenthinker_trade_database.MongoConnector import MongoConnector
        MongoConnector.get_instance().save_order(order=order_buy)
        Logger.log("Order executed in Sandbox mode")
        
    def sell(self,order_sell):
        from com_goldenthinker_trade_model.Symbol import Symbol
        s = Symbol(order_sell.get_symbol_str())
        Simulator._orders[s.uppercase_format()] = order_sell
        from com_goldenthinker_trade_database.MongoConnector import MongoConnector
        MongoConnector.get_instance().save_order(order=order_sell)
        Logger.log("Order executed in Sandbox mode")