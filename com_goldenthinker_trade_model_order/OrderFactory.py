import time
from com_goldenthinker_trade_datatype.CryptoFloat import CryptoFloat
from com_goldenthinker_trade_logger.Logger import Logger
from com_goldenthinker_trade_model_order.BuyMarketOrder import BuyMarketOrder
from com_goldenthinker_trade_model_order.SellMarketOrder import SellMarketOrder


class OrderFactory():
    
    
    _instance = None
    
    @classmethod
    def get_instance(cls):
        if cls._instance == None:
            cls._instance = OrderFactory()
        return cls._instance
    
    
    def generate_buy_order_from_quote_amount(self,amount):
        return BuyMarketOrder(amount=amount.get_symbol().closest_possible_amount_to_amount(amount.get_value()))
    
    def generate_buy_order_from_base_quantity(self,quantity):
        return BuyMarketOrder(quantity.get_symbol().get_current_price()*quantity)

    def generate_buy_order_from_signal(self,signal):
        return BuyMarketOrder(self.get_buy())
    
    def generate_buy_order_from_percentage(self,percentage):
        return BuyMarketOrder((percentage.get_symbol().min_amount_i_can_spend() + ( percentage.get_symbol().max_amount_i_can_spend() - percentage.get_symbol().min_amount_i_can_spend() )).percent(percentage))
          
    def generate_max_buy_order_for_symbol(self,symbol):
        return BuyMarketOrder(symbol.max_amount_i_can_spend())
    
    def generate_min_buy_order_for_symbol(self,symbol):
        return BuyMarketOrder(symbol.min_amount_i_can_spend())
    
    def generate_average_buy_order_for_symbol(self,symbol):
        return None
    
    def generate_sell_order_from_buy_order(self,buy_order):
        return None
    
    def generate_buy_order_from_sell_order(self,sell_order):
        return None
    
    def generate_sell_order_from_quote_amount(self,amount):
        return SellMarketOrder(amount=amount.get_symbol().closest_possible_amount_to_amount(amount.get_value()))

    def generate_sell_order_from_base_quantity(self,quantity):
        return SellMarketOrder(quantity.get_symbol().get_current_price()*quantity)

    def generate_sell_order_from_signal(self,signal):
        return SellMarketOrder(self.get_sell())
    
    def generate_sell_order_from_percentage(self,percentage):
        return SellMarketOrder((percentage.get_symbol().min_amount_i_can_spend() + ( percentage.get_symbol().max_amount_i_can_spend() - percentage.get_symbol().min_amount_i_can_spend() )).percent(percentage))
        
    def generate_max_sell_order_for_symbol(self,symbol):
        return SellMarketOrder(symbol.max_amount_i_can_spend())

    def generate_min_sell_order_for_symbol(self,symbol):
        return SellMarketOrder(symbol.min_amount_i_can_spend())
    
    def generate_average_sell_order_for_symbol(self,symbol):
        return None
    
        
    def generate_buy_order_from_analysis(self,amount_in_crypto_float,analysis):
        symbol = amount_in_crypto_float.get_symbol()
        qty_base_to_buy = 0
        try:                    
            self.current_quote_per_one_base = symbol.get_current_price()
        except Exception as e:
            print(e)
            Logger.log('Failed to get current price... retry in 5 seconds')
            time.sleep(5)
            self.current_quote_per_one_base = symbol.get_current_price()
        # Initialize rise and drop min, max and avg statistics for all rise and drop sequences
            
        self.max_delta_to_expect_rise = float(analysis['max_delta_rise_drop'][0]['max_delta'])
        self.min_delta_to_expect_rise = float(analysis['min_delta_rise_drop'][0]['min_delta'])
        
        self.max_delta_to_expect_drop = float(analysis['max_delta_rise_drop'][1]['max_delta'])
        self.min_delta_to_expect_drop = float(analysis['min_delta_rise_drop'][1]['min_delta'])
        
        # we take the average between the min expected rise and the min expected drop (usually everything drops)
        
        average_max_drop_min_rise = (self.min_delta_to_expect_rise + self.max_delta_to_expect_drop) / 2
        
        # if the worst case scenario is still higher than zero 
        # the create order
        amount_to_invest = CryptoFloat.get_neutral_element(symbol=symbol)
        if average_max_drop_min_rise > 0:
            balance = float(symbol.balance().get_value())
            percentage_of_balance_to_invest = symbol.percent_of_balance(symbol.what_percentage_is_another_number_of_myself(average_max_drop_min_rise))
            recommended_amount_to_invest = (CryptoFloat(symbol,balance).division(CryptoFloat(symbol,100)))*percentage_of_balance_to_invest
            if recommended_amount_to_invest > CryptoFloat(symbol,symbol.get_min_notional())*CryptoFloat(symbol,float_value=2.0):
                return BuyMarketOrder(quote_amt=recommended_amount_to_invest)
            else:
                return None
 
            
            
            
        
        
        #self.max_time_rise = analysis['max_delta_time_rise_drop'][0]['max_delta_time']
        #self.min_time_rise = analysis['min_delta_time_rise_drop'][0]['min_delta_time']

        #self.max_time_drop = analysis['max_delta_time_rise_drop'][1]['max_delta_time']
        #self.min_time_drop = analysis['max_delta_time_rise_drop'][1]['max_delta_time']

        #self.rise_vs_drops_qty = analysis['amount_of_drops_per_rises']
        
        #return None
    
