
from com_goldenthinker_trade_database.MongoConnector import MongoConnector
from com_goldenthinker_trade_exchange.ExchangeConfiguration import ExchangeConfiguration

from com_goldenthinker_trade_logger.Logger import Logger
from com_goldenthinker_trade_model_signals.BuySellSignal import BuySellSignal


Logger.set_process_name('gt_performance_backtesting')
Logger.terminal_output_enabled = True



exchange = ExchangeConfiguration.get_default_exchange()

    
    
all_signals = MongoConnector.get_instance().query_collection(collection_name='signals', query={})
all_signals_performance = MongoConnector.get_instance().query_collection(collection_name='signal_performance', query={})
MongoConnector.get_instance().create_unique_index_with_new_collection('signal_performance',unique_field_name='timestampt')
exclude_channels = ['cryptosignalscanner_results','btctradingresults','usdtradingresults','bnbtradingresults','ethtradingresults']

all_signals_performance_count = all_signals_performance.count()

while True:

    try:
        i = 0
        amt_signals = (all_signals.count())
        for s in all_signals:
            if i >= all_signals_performance_count:
                try:
                    if not s['channel'] in exclude_channels:
                        s1 = BuySellSignal(signal_dict=s,when_signal_ocurred=s['timestampt'],channel_name=s['channel'])
                        s1.performance()
                        Logger.log('Backtesting signal ' + str(i) + ' of ' + str(amt_signals))
                except Exception as e:
                    Logger.log(e.message)
            i = i + 1
        all_signals.close()
            
    except Exception as e:
        Logger.log(e.message)
