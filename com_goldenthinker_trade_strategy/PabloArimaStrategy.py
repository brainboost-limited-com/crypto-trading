from com_goldenthinker_trade_config.Config import Config
from com_goldenthinker_trade_datasource.DataSourceManager import DataSourceManager
from com_goldenthinker_trade_exchange.ExchangeConfiguration import ExchangeConfiguration
from com_goldenthinker_trade_logger.Logger import Logger
from com_goldenthinker_trade_monitor.Sequence import Sequence
from com_goldenthinker_trade_strategy.Strategy import Strategy
from com_goldenthinker_trader_robot.Robot import Robot
from com_goldenthinker_trade_portfolio.Portfolio import Portfolio



class PabloArimaStrategy(Strategy):
    
    def __init__(self,robot=None,data=None):
        super().__init__()    
    
    def start(self):
        while True:
            average_sequence_per_symbol_in_the_last_minutes_ds = DataSourceManager._data_sources['average_sequence_per_symbol_in_the_last_minutes']
            average_sequence_per_symbol_in_the_last_minutes_ds.subscribe(self)
            average_sequence_per_symbol_in_the_last_minutes_ds.start()
            
    def generate_buy_orders_for_quote_currency(self,data):
            
        exchange = ExchangeConfiguration.get_default_exchange()
        orders_to_execute = []
        portfolio = exchange.portfolio()
        if portfolio != None:
            portfolio_currencies = [k.upper() for k in list(portfolio.keys())]
            
            orders_from_analysis = []
            for d in data:
                for c in list(portfolio_currencies):
                    sym = d['symbol'].split('_')[1]
                    if (sym.find(c.upper())>0):
                        if c in sym:
                            if portfolio.get(c.lower())!=None:
                                from com_goldenthinker_trade_model.Symbol import Symbol
                                o = Portfolio.instance().generate_buy_order(Symbol(d['symbol'].split('_')[1]))
                                #o = BuyOrder(symbol=Symbol(d['symbol'].split('_')[1]),ptg=5)
                                if o is not None:
                                    orders_from_analysis.append(o)
        
            Logger.log('BUY SPOT MARKET ORDERS generated ')
            for prospective_order in orders_from_analysis:
                symbol = prospective_order.get_symbol()
                if symbol.get_symbol_quote_asset().upper() in portfolio_currencies:
                    try:
                        #existing_orders_for_symbol = exchange.get_all_orders(symbolß)
                        #if len(existing_orders_for_symbol)==0:              # only one order per symbol at a time
                        orders_to_execute.append(prospective_order)
                    except:
                        pass
                        #existing_orders_for_symbol = exchange.get_all_orders(symbol)


            

            with open("priority_symbols.list", "w") as myfile:
                ords = [o.get_symbol().uppercase_format() for o in orders_to_execute]
                o_str = (str(ords)[1:-1]).replace('\'','')
                Logger.log(o_str,telegram=True,public=True)
                myfile.write(o_str)



            for o in orders_to_execute:
                Robot.get_instance().buy(order=o)
                
            Logger.log('robot.py finished.')
        else:
            Logger.log('Portfolio not being properly returned')

    def deltas_average_variation(self,currency):
        
        tick_sequences = currency['tick_sequences']
        from com_goldenthinker_trade_datatype.CryptoDict import CryptoDict
        all_sequences_after_interval_time  = [CryptoDict(ts) for ts in tick_sequences if CryptoDict(ts).check_if_sequence_within_requested_time(int(Config.get('invest_interval_minutes'))) ]
        
        
        def count_volume_rise_from_right_to_left(seqs):
            
            def is_it_rising_volume(i,seqs):
                return (seqs[i].fuzzy_get('base_asset_volume_delta')>0) and (seqs[i].fuzzy_get('quote_asset_volume_delta')>0)
            
            consecutive_volume_rise = 0
            i = len(seqs)-1
            while (i >= 0 and is_it_rising_volume(i,seqs)): 
                consecutive_volume_rise = consecutive_volume_rise + 1
                i = i - 1
        
        volume_rise_count_right_to_left = count_volume_rise_from_right_to_left(all_sequences_after_interval_time)       
                
        
        rise_sequences = [ts for ts in all_sequences_after_interval_time if (ts.get_type()=='rise_sequence') ]
        drop_sequences = [ts for ts in all_sequences_after_interval_time if (ts.get_type()=='drop_sequence') ]
        
        
        amount_of_sequences = len(all_sequences_after_interval_time)
        amount_of_rise_sequences = len(rise_sequences)
        amount_of_drop_sequences = len(drop_sequences)
        
        
        avg_all_sequences_after_interval_time_sum = all_sequences_after_interval_time[0]
        for i in range(1,len(all_sequences_after_interval_time)):
             avg_all_sequences_after_interval_time_sum = avg_all_sequences_after_interval_time_sum + all_sequences_after_interval_time[i]
        avg_all_sequences_after_interval_time_sum = avg_all_sequences_after_interval_time_sum / amount_of_sequences
            

        avg_amount_of_rise_sequences = rise_sequences[0]
        for i in range(1,len(rise_sequences)):
             avg_amount_of_rise_sequences = avg_amount_of_rise_sequences + rise_sequences[i]
        avg_amount_of_rise_sequences = avg_amount_of_rise_sequences / amount_of_rise_sequences


        avg_amount_of_drop_sequences = drop_sequences[0]
        for i in range(1,len(drop_sequences)):
             avg_amount_of_drop_sequences = avg_amount_of_drop_sequences + drop_sequences[i]
        avg_amount_of_drop_sequences = avg_amount_of_drop_sequences / amount_of_drop_sequences

        #avg_all_sequences_after_interval_time_sum = sum(all_sequences_after_interval_time)/amount_of_sequences
        #avg_amount_of_rise_sequences = sum(rise_sequences)/amount_of_rise_sequences
        #avg_amount_of_drop_sequences = sum(drop_sequences)/amount_of_drop_sequences
                     
        return (avg_all_sequences_after_interval_time_sum,avg_amount_of_rise_sequences,avg_amount_of_drop_sequences,volume_rise_count_right_to_left) 
        
    @classmethod
    def should_i_sell_now_rising_sequence(self,sequence: Sequence):
        return False
        
    @classmethod
    def should_i_sell_now_dropping_sequence(self,sequence: Sequence):
        order_fees = 0 # we will calculate this later and depends on the exchange
        
        return ((len(sequence.ticks) >= sequence.drop_avg) and
        (sequence.anal['average_delta'] >= sequence.drop_avg_delta_sum-order_fees) and
        not sequence.is_volume_increasing())