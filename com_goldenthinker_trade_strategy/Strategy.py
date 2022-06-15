from com_goldenthinker_trade_config.Config import Config
from com_goldenthinker_trade_portfolio.Portfolio import Portfolio
from com_goldenthinker_trade_model_order.BuyMarketOrder import BuyMarketOrder
from com_goldenthinker_trader_robot.Robot import Robot
from com_goldenthinker_trade_exchange.ExchangeConfiguration import ExchangeConfiguration

from com_goldenthinker_trade_datasource.DataSourceManager import DataSourceManager
from com_goldenthinker_trade_strategy.CountryList import countries
from com_goldenthinker_trade_logger.Logger import Logger


import time

class Strategy:
        
        
    def __init__(self,robot=None,data=None):
        
        self.invest_interval_time = int(Config.get('invest_interval_minutes'))
        self.robot = robot
        self.real_time_ds = None
        self.data = data
        
        self.similar_past_slices = []
        
        
        self.accuracy = 0
        self.min_error = 0
        self.max_error = 0
        self.avg_error = 0

        
        # Obtain data from external sources web, apis , telegram
        self.sentiment = float(0)   # 0....1
        self.search_mentions_per_symbol = []
        self.search_engine_positive_words_per_symbol = []
        self.search_engine_negative_words_per_symbol = []
        self.social_media_positive_words_per_symbol = []
        self.social_media_negative_words_per_symbol = []
        self.market_indicator_per_symbol = []
        self.existing_signals = []
        self.previous_signals_and_accuracy = []
        self.multiple_exchanges_symbol_price = []
        self.trading_volume = 0
        self.goverment_regulatory_attacks_per_country = 0
        self.elon_musk = 0
        self.country_list = countries
        self.fiat_price = []
        

        # Rise sequences metrics 
        
        self.rise_avg_sequence_time = 0
        self.rise_shortest_sequence_time = 9999999
        self.rise_longest_sequence_time = 0
        self.rise_avg_delta_amt = 0
        self.rise_count = 0
        self.rise_highest_delta_amt = 0
        self.rise_lowest_delta_amt = 9999999
        self.rise_longest_sequence = 0
        self.rise_shortest_sequence = 9999999
        self.rise_highest_price = 0
        self.rise_lowest_price = 999999
        self.rise_avg_market_price = 0
        self.rise_time_hour = range(0,25)
        self.rise_time_min = range(0,61)
        self.rise_time_day = range(0,32)
        self.rise_time_montg = range(0,13)
        
        
                
        # Drop sequences metrics 
        
        self.drop_avg_sequence_time = 0
        self.drop_shortest_sequence_time = 9999999
        self.drop_longest_sequence_time = 0
        self.drop_avg_delta_amt = 0
        self.drop_count = 0
        self.drop_highest_delta_amt = 0
        self.drop_lowest_delta_amt = 9999999
        self.drop_longest_sequence = 0
        self.drop_shortest_sequence = 9999999
        self.drop_highest_price = 0
        self.drop_lowest_price = 999999
        self.drop_avg_market_price = 0
        self.drop_time_hour = range(0,25)
        self.drop_time_min = range(0,61)
        self.drop_time_day = range(0,32)
        self.drop_time_montg = range(0,13)
            
     

    def detect_symbol_that_raised_most(self):
        #for s in self.collection_names:
        pass
    

    def rising_up_reaction(self):
        pass
        

    def droppping_reaction(self):
        pass
        





    def get_rise_avg_sequence_time(self):
        return self.rise_avg_sequence_time
    
    def get_rise_shortest_sequence_time(self):
        return self.rise_shortest_sequence_time
    
    def get_rise_longest_sequence_time(self):
        return self.rise_longest_sequence_time
    
    def get_rise_avg_delta_amt(self):
        return self.drop_avg_delta_amt
    
    def get_rise_count(self):
        return self.rise_count
    
    def get_rise_highest_delta_amt(self):
        return self.rise_highest_delta_amt
    
    def get_rise_lowest_delta_amt(self):
        return self.rise_lowest_delta_amt
    
    def get_rise_longest_sequence(self):
        return self.rise_longest_sequence
    
    def get_rise_shortest_sequence(self):
        return self.rise_shortest_sequence
    
    def get_rise_highest_price(self):
        return self.rise_highest_price
    
    def get_rise_lowest_price(self):
        return self.rise_lowest_price
    
    def get_rise_avg_market_price(self):
        return self.rise_avg_market_price
    
    def get_rise_time_hour(self): 
        return self.rise_time_hour
    
    def get_rise_time_min(self):
        return self.rise_time_min
    
    def get_rise_time_day(self):
        return self.rise_time_day
    
    def get_rise_time_month(self):
        return self.rise_time_month
    
    def set_rise_avg_sequence_time(self,rise_avg_sequence_time):
        self.rise_avg_sequence_time = rise_avg_sequence_time
    
    def set_rise_shortest_sequence_time(self,rise_shortest_sequence_time):
        self.rise_shortest_sequence_time = rise_shortest_sequence_time
    
    def set_rise_longest_sequence_time(self,rise_longest_sequence_time):
        self.rise_longest_sequence_time = rise_longest_sequence_time
    
    def set_rise_avg_delta_amt(self,rise_avg_delta_amt):
        self.drop_avg_delta_amt = rise_avg_delta_amt
    
    def set_rise_count(self,rise_count):
        self.rise_count = rise_count
    
    def set_rise_highest_delta_amt(self,rise_highest_delta_amt):
        self.rise_highest_delta_amt = rise_highest_delta_amt
    
    def set_rise_lowest_delta_amt(self,rise_lowest_delta_amt):
        self.rise_lowest_delta_amt = rise_lowest_delta_amt
    
    def set_rise_longest_sequence(self,rise_longest_sequence):
        self.rise_longest_sequence = rise_longest_sequence
    
    def set_rise_shortest_sequence(self,rise_shortest_sequence):
        self.rise_shortest_sequence = rise_shortest_sequence
    
    def set_rise_highest_price(self,rise_highest_price):
        self.rise_highest_price = rise_highest_price
    
    def set_rise_lowest_price(self,rise_lowest_price):
        self.rise_lowest_price = rise_lowest_price
    
    def set_rise_avg_market_price(self,rise_avg_market_price):
        self.rise_avg_market_price = rise_avg_market_price
    
    def set_rise_time_hour(self,rise_time_hour): 
        self.rise_time_hour = rise_time_hour
    
    def set_rise_time_min(self,rise_time_min):
        self.rise_time_min = rise_time_min
    
    def set_rise_time_day(self,rise_time_day):
        self.rise_time_day = rise_time_day
    
    def set_rise_time_month(self,rise_time_month):
        self.rise_time_month = rise_time_month
    
        
        
        
        
        
    def get_drop_avg_sequence_time(self):
        return self.drop_avg_sequence_time
    
    def get_drop_shortest_sequence_time(self):
        return self.drop_shortest_sequence_time
    
    def get_drop_longest_sequence_time(self):
        return self.drop_longest_sequence_time
    
    def get_drop_avg_delta_amt(self):
        return self.drop_avg_delta_amt
    
    def get_drop_count(self):
        return self.drop_count
    
    def get_drop_highest_delta_amt(self):
        return self.drop_highest_delta_amt
    
    def get_drop_lowest_delta_amt(self):
        return self.drop_lowest_delta_amt
    
    def get_drop_longest_sequence(self):
        return self.drop_longest_sequence
    
    def get_drop_shortest_sequence(self):
        return self.drop_shortest_sequence
    
    def get_drop_highest_price(self):
        return self.drop_highest_price
    
    def get_drop_lowest_price(self):
        return self.drop_lowest_price
    
    def get_drop_avg_market_price(self):
        return self.drop_avg_market_price
    
    def get_drop_time_hour(self):
        return self.drop_time_hour
    
    def get_drop_time_min(self):
        return self.drop_time_min
    
    def get_drop_time_day(self):
        return self.drop_time_day
    
    def get_drop_time_montg(self):
        return self.drop_time_montg
    
    def set_drop_avg_sequence_time(self,drop_avg_sequence_time):
        self.drop_avg_sequence_time = drop_avg_sequence_time
    
    def set_drop_shortest_sequence_time(self,drop_shortest_sequence_time):
        self.drop_shortest_sequence_time = drop_shortest_sequence_time
    
    def set_drop_longest_sequence_time(self,drop_longest_sequence_time):
        self.drop_longest_sequence_time = drop_longest_sequence_time
    
    def set_drop_avg_delta_amt(self,drop_avg_delta_amt):
        self.drop_avg_delta_amt = drop_avg_delta_amt
    
    def set_drop_count(self,drop_highest_delta_amt):
        self.drop_highest_delta_amt = drop_highest_delta_amt
    
    def set_drop_highest_delta_amt(self,drop_highest_delta_amt):
        self.drop_highest_delta_amt = drop_highest_delta_amt
    
    def set_drop_lowest_delta_amt(self,drop_shortest_sequence):
        self.drop_shortest_sequence = drop_shortest_sequence
    
    def set_drop_longest_sequence(self,drop_shortest_sequence):
        self.drop_longest_sequence = drop_shortest_sequence
    
    def set_drop_shortest_sequence(self,drop_shortest_sequence):
        self.drop_shortest_sequence = drop_shortest_sequence
    
    def set_drop_highest_price(self,drop_highest_price):
        self.drop_highest_price = drop_highest_price
    
    def set_drop_lowest_price(self,drop_lowest_price):
        self.drop_lowest_price = drop_lowest_price
    
    def set_drop_avg_market_price(self,drop_avg_market_price):
        self.drop_avg_market_price = drop_avg_market_price
    
    def set_drop_time_hour(self,drop_time_hour):
        self.drop_time_hour = drop_time_hour
    
    def set_drop_time_min(self,drop_time_min):
        self.drop_time_min = drop_time_min
    
    def set_drop_time_day(self,drop_time_day):
        self.drop_time_day = drop_time_day
    
    def set_drop_time_montg(self,drop_time_montg):
        self.drop_time_montg = drop_time_montg
        
        
     
    # 1- Obtains real time market data from different cryprocurrency exchanges (binance by default)  (DONE)
     
   
    # 1.1- Pulls data from the last minutes sequences from all cryptocurrencies                      (DONE)
    # 1.2- Organises market data into rising seaquences and dropping seecuences for each symbol      (DONE)
    # 1.3- Generates cross-currency setting repetition patterns when a currency rises or drops (for example when there is crisis, gold rises)  (LATER)
   
   
    
    # 2- finds best invetsment opportunities analysing the market data mathematically      (ONGOING)
   
   
    
    # 2.1- Calculates averages for all sequences values rising, dropping and 'rising-dropping' sequences, sequence length, sequence deltas...   (FIXING)
    # 2.2- Finds the top opportunities in the last X minutes mathematically.                (FIXING)
   
   
    # 2.3- Obtains information from different sources crossing information and adding probabilistic sentiment to the mathematical analysis about 4 times per day   (PARTIALLY)
   
   
   
    # 2.3.1-    Crosses information between Telegram obtained signals issued by trader professionals to see see current sentiment    (DONE)
    # 2.3.2-        Prioritises success probability from the different telegram traders according their success factor calculation from backtesting their preious signals     (DONE HAVE TO FIX)
    # 2.3.3-    Crosses information triggering google serp searches for each of the different currencies and calculates sentiment value, (a multiplier ranging from (0-1) )   (PARTIALLY DONE NEEDS ADAPTATION)
    # 2.3.4-    Croses information detected from social media with regards to sentiment like Elon Musk posts on twitter
    # 2.3.5-        Calculates sentiment for each currency by counting positive and negative keywords and phrases in the last news (Rumours, Currency Depreciation, Goverment attacks)
      
    
    
    # 3- Executes buy orders according previous information obtained from the previous mathematical analysis and empirical data sources     (ORDERS EXECUTED BUT INTEGRATION WITH THE REST ONGOING)
    
    
    
    # 3.1- Triggers Buy orders along with individual cocurrent monitors for each orders prioritising market streaming data for the ongoing order. 
    # 3.2- Each order monitor works independently monitoring if the orders are making money as predicted on real time.      (DONE)
    # 3.3- If the monitor finds the calculations went wrong and are not making money, sells to stop the loss.
    
    
    
    # 4- Learning from the errors
    
    
    
    # 4.1-  Finds all data sources that were involved in the order not going well. 
    # 4.2-  Adds a lower priority flag with an index on how wrong was the data source. 
    # 4.3-  Anotates those money loosing orders for future heads up when a similar calculation pattern comes
    # 4.4-  Repeats step 2 on
    
    def subscribe(self,robot):
        self.robot = robot
    
        
    def notify(self,data):
        self.update(data)
        self.generate_buy_orders_for_quote_currency(data)
        print("NOTIFY_Strategy: " + str(data))
    
    
    
    def update(self,data):
        # Obtain symbold from data and check if there was not any recent Telegram Signal with regards to those symbols
        # Symbols came already sorted by: 
        # 
        #                               The biggest rise average delta
        #                               The lowest  rise average delta 
        #                               The volume delta (the more delta means that is going to rise) 
        #                               Now we will cross this `with the Telegram signals that come from many
        #                                    different sources to see if there is any rumours about the currency 
        #                                    or any existing ongoing signal
        self.robot.notify(data)

    
    
        
    def start(self):
        pass
            
    
    
    
        
        
        

    
    