from com_goldenthinker_trade_datasource.AverageSequenceDataSource import AverageSequenceDataSource
from datetime import datetime,timedelta

from com_goldenthinker_trade_datasource.OnDemandDataSource import OnDemandDataSource
from com_goldenthinker_trade_database.MongoConnector import MongoConnector
from com_goldenthinker_trade_datasource.LastMinuteSymbolStreamDataSource import LastMinuteSymbolStreamDataSource
from decimal import Decimal

from com_goldenthinker_trade_datasource.TwitterOnDemandDataSource import TwitterOnDemandDataSource
from com_goldenthinker_trade_config.Config import Config

class DataSourceManager:
    
    
    
    _data_sources = dict()
    _config = Config.read_config()
    
    mongo_ssh = OnDemandDataSource(name=_config.get('service_instance_name_1_2'),trust=Decimal(0.99999999),session=MongoConnector.get_instance())
    _data_sources[mongo_ssh.get_name()] = mongo_ssh
    
    mongo_atlas = OnDemandDataSource(name=_config.get('service_instance_name_1_2'),trust=Decimal(0.99999999),session=MongoConnector.get_instance())
    _data_sources[mongo_atlas.get_name()] = mongo_atlas
    
    from com_goldenthinker_trade_datasource.MonitorAllSymbolsRealTimeDataSource import MonitorAllSymbolsRealTimeDataSource
    gt_monitor_all_symbols = MonitorAllSymbolsRealTimeDataSource()
    _data_sources[gt_monitor_all_symbols.get_name()] = gt_monitor_all_symbols
    
    
    monitor_last_minutes_sequences = LastMinuteSymbolStreamDataSource(name='last_min_sequences_all_symbols',minutes_ago=15)
    _data_sources[monitor_last_minutes_sequences.get_name()] = monitor_last_minutes_sequences
    
    average_sequence_for_each_symbol_in_the_last_minutes = AverageSequenceDataSource('average_sequence_per_symbol_in_the_last_minutes')
    _data_sources[average_sequence_for_each_symbol_in_the_last_minutes.get_name()] = average_sequence_for_each_symbol_in_the_last_minutes
    
    twitter_data_source = TwitterOnDemandDataSource.get_instance()
    _data_sources['twitter'] = twitter_data_source
    
    
    
    @classmethod
    def subscribe(cls,name,observer):
        cls._data_sources[name].subscribe(observer)
    
    @classmethod
    def get_data_source(cls,name):
        return cls._data_sources.get(name)