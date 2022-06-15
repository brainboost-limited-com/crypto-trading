from com_goldenthinker_trade_datatype.CryptoFloat import CryptoFloat
from com_goldenthinker_trade_logger.Logger import Logger
import traceback





class Robot:


    _instance = None


    # Configuration
    _use_volume = False
    

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = Robot()
        return cls._instance

    def __init__(self):
        self.strategy = None
    
    def subscribe(self,strategy):
        self.strategy = Strategy
        self.strategy.start(self)
    
    
    def notify(self, data):
        print("ROBOT REECEIVED: ")
        print("================")
        print(str(data))
        
    def study(self):
        self.real_time_market_data_processing()
        
        
    def buy(self,order=None):
        try:
            if order is not  None:
                result = order.execute()
                # buys order
                # monitors order passing self as argument, so the monitors as well as the Strategy give intructions to the robot
                if result is not None:
                    Logger.log("I bought " + str(order.get_quote_amt()) + " worth of " + str(order.get_symbol()) + " balance " + str(order.get_symbol().balance()),telegram=True)
                    Logger.log("Monitoring " + str(order.get_quote_amt().get_symbol()))
                    #from com_goldenthinker_trade_datasource.MonitorSpecificSymbolsRealTimeDataSource import MonitorSpecificSymbolsRealTimeDataSource    
                    # monitor_for_symbol_data_source = MonitorSpecificSymbolsRealTimeDataSource(order.get_quote_amt().get_symbol())
                    # monitor_for_symbol_data_source.subscribe(self)
                    # monitor_for_symbol_data_source.start()
                else:
                    Logger.log("Failed to buy, as error: " + str(result))
        except Exception as e:
            Logger.log(e)
            Logger.log(traceback.format_exc())
                
                
    
    def sell(self,amount=None,order=None):
        if order is None and amount is not None:
            
            from com_goldenthinker_trade_model_order.SellMarketOrder import SellMarketOrder
            o = SellMarketOrder(amount=amount)
            
            o.execute()

            Logger.log("I sold " + str(amount) + " worth of " + str(amount.get_symbol()),telegram=True)
        else:
            order.execute()
