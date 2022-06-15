from com_goldenthinker_trade_datatype.CryptoFloat import CryptoFloat

class OrderScheduler:
    
    _instance = None
    
    @classmethod
    def get_instance(cls):
        cls._instance.queue = dict()
        def get_portfolio_balances():
            from com_goldenthinker_trade_exchange.ExchangeConfiguration import ExchangeConfiguration
            return ExchangeConfiguration.get_default_exchange().portfolio()
        cls._instance.balance = get_portfolio_balances()
        cls._instance.symbol_frequency = dict()
        
        
        
    def prepare_balance(self, order):
        return True
        #symbol = order.get_signal().get_symbol()
        
        # def compute_currency_frequency():
        #     currency = symbol.symbol_b().lower()
        #     if self.symbol_frequency.get(currency) == None:
        #         self.symbol_frequency[currency] = 0
        #     else:
        #         self.symbol_frequency[currency] = self.symbol_frequency[currency] + 1
                
        
        # def convert_money_from_portfolio_to_fullfill_order():
        #     # we will prioritize the conversion of the least frequently used
        #     # currencies into the most frequently used ones
        #     # so we have enough balance to execute the order
        #     return True
        
        
        # compute_currency_frequency()
        # convert_money_from_portfolio_to_fullfill_order()
        
        # balance_to_execute_order = CryptoFloat(symbol,self.balance[symbol.symbol_b()])
        # enough_to_cover_symbol_min = CryptoFloat(symbol,symbol.min_quantity_i_can_buy())
        # if (balance_to_execute_order >= enough_to_cover_symbol_min):
        #     return True
        # else:
        #     return convert_money_from_portfolio_to_fullfill_order()

        
    def schedule_buy(self,buy_order):
        if self.prepare_balance(buy_order):
            self.queue[buy_order.generate_id()] = buy_order
        
    
    def schedule_sell(self,sell_order):
        if self.prepare_balance(sell_order):
            self.queue[sell_order.generate_id()] = sell_order
    
    def schedule_buy_sell(self,buy_sell_order):
        if self.prepare_balance(buy_sell_order):
            self.queue[buy_sell_order.generate_id()] = buy_sell_order
        
    
    