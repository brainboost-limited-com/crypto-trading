from com_goldenthinker_trade_config.Config import Config
from com_goldenthinker_trade_datasource.DataSource import DataSource
from com_goldenthinker_trade_database.MongoConnector import MongoConnector
from com_goldenthinker_trade_datatype.CryptoDict import CryptoDict
from datetime import datetime
# DataSource that obtains the average sequence for each symbol in the last minute

class AverageSequenceDataSource(DataSource):
    
    def __init__(self, name):
        super().__init__(name)
        self.invest_interval_time = int(Config.get('invest_interval_minutes'))
   
    def obtain_collection_names(self):
        return MongoConnector.get_instance().list_collection_names()
    
    
    
    def average_sequence_per_symbol(self):
        
        def count_volume_rise_from_right_to_left(seqs):
            
            def is_it_rising_volume(i,seqs):
                return (seqs[i]['base_asset_volume_delta']>0) and (seqs[i]['quote_asset_volume_delta']>0)
            
            
            consecutive_volume_rise = 0
            base_asset_volume_delta = 0
            quote_asset_volume_delta = 0
            i = len(seqs)-1
            while (i >= 0 and is_it_rising_volume(i,seqs)): 
                consecutive_volume_rise = consecutive_volume_rise + 1
                base_asset_volume_delta = base_asset_volume_delta + seqs[i]['base_asset_volume_delta']
                quote_asset_volume_delta = quote_asset_volume_delta + seqs[i]['quote_asset_volume_delta']
                i = i - 1
            if len(seqs)>0:
                last_symbol_total_volume  =  float(seqs[0]['sequence'][0]['data']['v'])  # We do not want to invest in symbols with not so much volume as if there is a drop will take long to recover
                return (consecutive_volume_rise,base_asset_volume_delta,quote_asset_volume_delta,last_symbol_total_volume)
            else:
                return (consecutive_volume_rise,base_asset_volume_delta,quote_asset_volume_delta)
                
        
        def sum_sequence(*args):
            analysis_sum = None
            list_result = []

            for each_symbol in args[0]:
                symbol_and_sum_analysis = dict()
                symbol_and_sum_analysis['symbol'] = each_symbol.get('symbol')
                last_min_sequences = each_symbol.get('data')
                
                volume = count_volume_rise_from_right_to_left(last_min_sequences)
                
                
                analysis_sum = None
                for i,each_sequence in enumerate(last_min_sequences):
                    current_analysis = each_sequence.get('analysis')
                    if current_analysis!=None:
                        if i==0:
                            analysis_sum = CryptoDict(current_analysis)
                        else:
                            analysis_sum = analysis_sum + CryptoDict(each_sequence.get('analysis'))      
                symbol_and_sum_analysis['analysis'] = analysis_sum
                symbol_and_sum_analysis['amt_seqs'] = len(last_min_sequences)
                symbol_and_sum_analysis['volume'] = volume
                if len(last_min_sequences) > 0:
                    list_result.append(symbol_and_sum_analysis)
                    
                # sorted_by_average_delta
            try:
                list_result.sort(key=lambda x: x['volume'][3], reverse=True)
            except:
                pass
            list_result.sort(key=lambda x: (x['analysis'].fuzzy_get('max_tick_value')-x['analysis'].fuzzy_get('min_tick_value')), reverse=True)  # --->  Then sorts by higher delta price 
            list_result.sort(key=lambda x: x['analysis'].fuzzy_get('biggest_delta'),reverse=True)                                                # --->  Sorts by the worst delta in price descending order
            list_result.sort(key=lambda x: x['volume'][1], reverse=True)                                                                         # --->  Sorts by higher base asset volume delta (volume has increased the most)
            list_result.sort(key=lambda x: x['analysis'].fuzzy_get('max_delta_time'),reverse=True)                                               # --->  Sorts by the time it took to achieve the best delta (the shorter time it takes to make money the better)
            
            list_result_no_0000 = [r for r in list_result if r['volume']!=(0,0,0) and r['volume']!=(0,0,0,0)]      # Filters our sequences of only one single element that are
                    
            return list_result_no_0000
            
        # db.getCollection('binance_WRXEUR').find({ timestampt: {$gt: (new Date(ISODate().getTime() - 1000 * 60 * 60 * (15 + 60)  )) } })
        symbol_stats_in_the_last_minutes = []
        self.collection_names = self.obtain_collection_names()

        start_query = datetime.now() 
        latest_sequences_for_symbol_within_x_minutes = MongoConnector.get_instance().get_all_data_in_the_last_minutes_for_all_symbols()
        end_query = datetime.now()
        
        
            
        seq_sum = sum_sequence(latest_sequences_for_symbol_within_x_minutes)
        for sum_symbol in seq_sum:
            statistical_data_in_the_last_minutes = dict()
            avg_seq = sum_symbol['analysis']/sum_symbol.get('amt_seqs')
            statistical_data_in_the_last_minutes['symbol'] = sum_symbol['symbol']
            statistical_data_in_the_last_minutes['avg_sequence'] = avg_seq
            symbol_stats_in_the_last_minutes.append(statistical_data_in_the_last_minutes)
        
        return symbol_stats_in_the_last_minutes

       

    
    def start(self):
        data = self.average_sequence_per_symbol()
        self.update(data)