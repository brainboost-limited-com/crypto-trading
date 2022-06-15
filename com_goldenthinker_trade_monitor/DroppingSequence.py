from com_goldenthinker_trade_datatype.CryptoFloat import CryptoFloat

from numpy import mean
from com_goldenthinker_trade_monitor.Sequence import Sequence
from com_goldenthinker_trade_database.MongoConnector import MongoConnector
import datetime
from com_goldenthinker_trade_strategy.StrategyHub import StrategyHub

from com_goldenthinker_trader_robot.Robot import Robot


class DroppingSequence(Sequence):
    
    def __init__(self,monitor=None,first_tick=None,next_sequence=None,previous_sequence=None):
        super().__init__(monitor,first_tick,next_sequence,previous_sequence)
        self.type = 'drop'
        self.option = 'monitor_script'
        self.symbol = self.monitor.get_symbol()
        
        
    def to_dict(self):
        seq = dict()
        seq['timestampt'] = datetime.datetime.utcnow()
        seq['type'] = 'drop_sequence'
        seq['len'] = len(self.ticks)
        sum_deltas = 0
        for d in self.ticks:
            sum_deltas = sum_deltas + d.get_delta()
        seq['delta_sum'] = sum_deltas
        seq['analysis'] = self.analyze()
        if len(self.ticks) >= 2:
            seq['seq_time'] = (self.ticks[(len(self.ticks)-1)].get_timestampt() - self.ticks[0].get_timestampt()).total_seconds()
        seq['sequence'] = [t.to_dict() for t in self.ticks]
        seq['base_asset_volume_delta'] = (self.ticks[(len(self.ticks)-1)].get_total_traded_base_asset_volume() - self.ticks[0].get_total_traded_base_asset_volume()).get_value()
        seq['quote_asset_volume_delta'] = (self.ticks[(len(self.ticks)-1)].get_total_traded_quote_asset_volume() - self.ticks[0].get_total_traded_quote_asset_volume()).get_value()
        return seq


    def __str__(self):
        return str(self.to_dict())
    
    
    def add_tick(self,tick):
        if tick < self.last_tick():
            self.ticks.append(tick)
            self.anal = self.analyze()
            if (self.should_i_sell_now() and self.option=='orders_script'):
                Robot.instance().sell(amount=CryptoFloat(self.symbol.uppercase_format(),self.symbol.balance()))
            return self
        else:
            from com_goldenthinker_trade_monitor.RisingSequence import RisingSequence
            rs = RisingSequence(monitor=self.monitor,first_tick=tick,previous_sequence=self,next_sequence=None)
            self.next(rs)
            print(str(self))
            #MongoConnector.get_instance().insert_sequence_into_new_document_or_push_to_existing(sequence=self.to_dict(),symbol=self.monitor.get_symbol().uppercase_format())
            from com_goldenthinker_trade_exchange.ExchangeConfiguration import ExchangeConfiguration
            MongoConnector.get_instance().insert_sequence(sequence=self.to_dict(),symbol=self.monitor.get_symbol().uppercase_format(),exchange=ExchangeConfiguration.get_default_exchange_name())
            return rs
        
        
    def analyze(self):
        analysis = dict()
        analysis['min_tick_value'] = min([d.get_value() for d in self.ticks])
        analysis['max_tick_value'] = max([d.get_value() for d in self.ticks])
        analysis['avg_tick_value'] = mean([d.get_value() for d in self.ticks])
        analysis['total_delta_tick_value'] = float(self.ticks[len(self.ticks)-1].get_value()) - float(self.ticks[0].get_value())
        
        analysis['max_tick_value_timestampt'] = self.ticks[0].get_timestampt()
        analysis['min_tick_value_timestampt'] = self.ticks[len(self.ticks)-1].get_timestampt()
        analysis['sequence_duration'] = (analysis['max_tick_value_timestampt'] - analysis['min_tick_value_timestampt']).total_seconds()
        
        analysis['avg_tick_value_time'] = mean([d.get_delta_time() for d in self.ticks])


        analysis['biggest_delta'] = self.ticks[len(self.ticks)-1].get_delta()
        analysis['smallest_delta'] = self.ticks[0].get_delta()
        analysis['average_delta'] = mean([d.get_delta() for d in self.ticks])
        
        analysis['average_delta_time'] = abs(mean([d.get_delta_time() for d in self.ticks]))
        analysis['max_delta_time'] = abs(max([d.get_delta_time() for d in self.ticks]))
        return analysis
        
        
    def get_type(self):
        return self.type

    def get_base_asset_volume_delta(self):
        try:
            base_asset_volume_delta = self.anal['base_asset_volume_delta']
            return base_asset_volume_delta
        except Exception as e:
            return 0
    
    def get_quote_asset_volume_delta(self):
        try:
            quote_asset_volume_delta = self.anal['quote_asset_volume_delta']
            return quote_asset_volume_delta
        except Exception as e:
            return 0
            
    
    def is_volume_increasing(self):
        if self.prev()!=None:
            if self.prev().get_base_asset_volume_delta() != 0 and self.get_base_asset_volume_delta() != 0:
                return (self.prev().get_base_asset_volume_delta() < self.get_base_asset_volume_delta())
            else:
                return False
        else:
            return False
        
    # Sells if and only if the length of the dropping sequence is longer than the
    # average droppping sequence 
    # the current price difference in this dropping sequence is higher than the price drop in an average dropping sequence
    # and if the traded volume of the base asset is not increasing in the current sequence. 
    
    def should_i_sell_now(self):
        return StrategyHub.strategy_to_use().should_i_sell_now_dropping_sequence(self)
