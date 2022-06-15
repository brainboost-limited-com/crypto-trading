import datetime
import sys

from com_goldenthinker_trade_monitor.Tick import Tick

if 'com_goldenthinker_trade_datatype.CryptoFloat' not in sys.modules:
    from com_goldenthinker_trade_datatype.CryptoFloat import CryptoFloat
import sys

if 'com_goldenthinker_trade_model.Symbol' not in sys.modules:
    from com_goldenthinker_trade_model.Symbol import Symbol


    # Kline data is as follows
    #[
    #  [
    #1499040000000,      // Open time
    #"0.01634790",       // Open
    #"0.80000000",       // High
    #"0.01575800",       // Low
    #"0.01577100",       // Close
    #"148976.11427815",  // Volume
    #1499644799999,      // Close time
    #"2434.19055334",    // Quote asset volume
    #308,                // Number of trades
    #"1756.87402397",    // Taker buy base asset volume
    #"28.46694368",      // Taker buy quote asset volume
    #"17928899.62484339" // Ignore.
#  ]
#]

class Kline:
    
    
    def __init__(self,symbol,kline):
        if type(symbol)==str:
            symbol_str = symbol
            from com_goldenthinker_trade_model.Symbol import Symbol
            symbol = Symbol(symbol_str)
        self.symbol = symbol
        self.opentime=(datetime.datetime.fromtimestamp(int(kline[0])/1000)).replace(tzinfo=None)
        from com_goldenthinker_trade_datatype.CryptoFloat import CryptoFloat
        self.open=CryptoFloat(symbol.lowercase_format_slashed(),kline[1])
        self.high=CryptoFloat(symbol.lowercase_format_slashed(),kline[2])
        self.low=CryptoFloat(symbol.lowercase_format_slashed(),kline[3])
        self.close=CryptoFloat(symbol.lowercase_format_slashed(),kline[4])
        self.volume=CryptoFloat(symbol.lowercase_format_slashed(),kline[5])
        self.close_time=(datetime.datetime.fromtimestamp(int(kline[6])/1000)).replace(tzinfo=None)
        self.quote_asset_volume=CryptoFloat(symbol.lowercase_format_slashed(),kline[7])
        self.number_of_trades=int(kline[8])
        self.taker_buy_asset_volume = CryptoFloat(symbol.lowercase_format_slashed(),kline[9])
        self.taker_buy_quote_asset_volume = CryptoFloat(symbol.lowercase_format_slashed(),kline[10])
        self.ignore = CryptoFloat(symbol.lowercase_format_slashed(),kline[11])
        
    def is_kline_inside_entry_range(self,entry_range):
        return self.open in entry_range

    def is_kline_inside_target(self,target_range):
        return self.high in target_range
        
    def is_kline_below_stop_loss(self,stop_range):
        return self.low not in stop_range
    
    def return_profit(self,target_range):
        if self.is_kline_inside_target(target_range):
            return (self.open - target_range.a)
        else:
            return CryptoFloat(self.symbol,0)
    
    def return_loss(self,stop_range):
        if self.is_kline_below_stop_loss(stop_range):
            return (self.low - stop_range.a)
        else:
            return CryptoFloat(self.symbol,0)
        
    def to_tick(self,time_units):
        data = dict()
        data['e'] = time_units
        data['E'] = self.opentime
        data['s'] = self.symbol
        data['p'] = self.open - self.close   # price change
        if (self.open.get_value() - self.close.get_value())!=0:
            data['P'] = CryptoFloat(symbol=self.symbol,float_value=(100 / (self.open.get_value() / (self.open.get_value() - self.close.get_value()))))
        else:
            data['P'] = 0
        data['w'] = CryptoFloat(symbol=self.symbol,float_value=(self.open.get_value() + self.close.get_value() / 2))
        data['x'] = self.open
        data['c'] = self.close
        data['Q'] = 1
        data['b'] = self.close
        data['B'] = 1
        data['a'] = self.low
        data['A'] = 1
        data['o'] = self.open
        data['h'] = self.high
        data['l'] = self.low
        data['v'] = self.volume
        data['q'] = self.quote_asset_volume
        data['O'] = self.opentime
        data['C'] = self.close_time
        data['F'] = None
        data['L'] = None
        data['n'] = self.number_of_trades
        tick = Tick(data)
        return tick