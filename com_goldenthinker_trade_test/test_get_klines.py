
from com_goldenthinker_trade_database.MongoConnector import MongoConnector
from com_goldenthinker_trade_exchange.ExchangeConfiguration import ExchangeConfiguration

from com_goldenthinker_trade_logger.Logger import Logger
from com_goldenthinker_trade_model_signals.BuySellSignal import BuySellSignal


Logger.set_process_name('signal_performance')



exchange = ExchangeConfiguration.get_default_exchange()

    
    
all_signals = MongoConnector.get_instance().query_collection(collection_name='signals', query={})
MongoConnector.get_instance().create_unique_index_with_new_collection('signal_performance',unique_field_name='timestampt')

for s in all_signals:
    #d = Date(date_str=s['timestampt'])
    #e = d.add_days(amount_of_days=2)
    s1 = BuySellSignal(signal_dict=s,when_signal_ocurred=s['timestampt'],channel_name=s['channel'])
    print(str(s1.performance()))
    #print(str(d))
    #print(str())