
from com_goldenthinker_trade_database.MongoConnector import MongoConnector
from com_goldenthinker_trade_exchange.BinanceExchange import BinanceExchange
from com_goldenthinker_trade_logger.Logger import Logger
from com_goldenthinker_trade_model.Symbol import Symbol
from com_goldenthinker_trade_model_signals.Signal import Signal
from com_goldenthinker_trade_model_order.BuySellMarketOrder import BuySellMarketOrder
from com_goldenthinker_trade_datatype.CryptoFloat import CryptoFloat
from com_goldenthinker_trade_datatype.RangeCryptoFloat import RangeCryptoFloat
from com_goldenthinker_trade_utils.Date import Date
from com_goldenthinker_trade_utils.Utils import Utils
from com_goldenthinker_trade_scheduler.OrderScheduler import OrderScheduler
import datetime



class BuySellSignal(Signal):
        
    def __init__(self,signal_dict=None,when_signal_ocurred=None,channel_name=None):
        super().__init__(signal_dict,when_signal_ocurred,channel_name)

        
    def generate_id(self):
        super().generate_id()
    
    def is_worth_to_execute(self):
        print("Analizing previous data on this signal...")
        return True
    
    def profit(self):
        return (CryptoFloat(self.symbol,self.signal['sell']) - CryptoFloat(self.symbol,self.signal.buy))
    
    
    def execute(self):
        o = BuySellMarketOrder(self)
        OrderScheduler.get_instance().schedule_buy_sell(o)
        return True
    
    
    def profit_forecast(self,signal):
        return (CryptoFloat(self.symbol,signal.sell) - CryptoFloat(self.symbol,signal.buy))
    

    def get_buy(self):
        if self.signal.get('buy')!=None:
            return RangeCryptoFloat(self.get_buy_a(),self.get_buy_b())
        else:
            return None
        
        
    def get_buy_price(self):
        pass
    
    def get_sell(self):
        if self.signal.get('sell')!=None:
            return RangeCryptoFloat(self.get_sell_a(),self.get_sell_b())
        else:
            return None

        
    
    def get_stop(self):
        if self.signal.get('stoploss')!=None:
            return RangeCryptoFloat(CryptoFloat(self.get_symbol(),self.signal['stop']))
        else:
            return None
    
    
    def has_symbol(self):
        return self.signal.get('symbol')!=None
    
    def has_buy(self):
        return self.signal.get('buy')!=None
    
    def has_sell(self):
        return self.signal.get('sell')!=None
        
    def has_stop_loss(self):
        return self.signal.get('stoploss')!=None
    
    def valid(self):
        return self.has_symbol() and (self.has_buy() and self.has_sell())
    
    
    def get_buy_a(self):
        if self.signal.get('buy')!=None:
            try:
                return CryptoFloat(self.get_symbol(),float(self.signal['buy'][0]['numbers'][0]))
            except IndexError:
                return None
        else:
            return None
    
    def get_buy_b(self):
        if self.signal.get('buy')!=None:
            try:
                return CryptoFloat(self.get_symbol(),float(self.signal['buy'][0]['numbers'][1]))
            except IndexError:
                return None
        else:
            return None
    
    def get_sell_a(self):
        if self.signal.get('sell')!=None:
            try:
                return CryptoFloat(self.get_symbol(),float(self.signal['sell'][0]['numbers'][0]))
            except IndexError:
                return None
        else:
            return None
    
    def get_sell_b(self):
        if self.signal.get('sell')!=None:
            try:
                return CryptoFloat(self.get_symbol(),float(self.signal['sell'][0]['numbers'][1]))
            except IndexError:
                return None
        else:
            return None
    
    def get_stop_loss(self):
        self.signal = Utils().group_dict_by(self.signal,'stoploss')
        if self.has_stop_loss():
            return RangeCryptoFloat(a=CryptoFloat(self.get_symbol(),self.signal['stoploss'][0]))
        else:
            return None
        
    def get_exchange(self):
        if self.signal.get('stoploss')!=None:
            return str(self.signal['exchange']['words_in_signal_line'][0])
        else:
            return None
    
    def set_profit(self,profit):
        self.signal['profit'] = profit.get_float_as_string()
    
    def set_loss(self,loss):
        self.signal['stoploss'] = loss.get_float_as_string()
        
    def calculate_loss(self):
        return super().calculate_loss()
    
    def calculate_profit(self):
        return super().calculate_profit()
    
        
    def calculate_profit_and_loss(self,limit_days=10):
        date_a = Date(date_str=self.signal['timestampt'])
        date_b = date_a.add_days(limit_days)
        klines = BinanceExchange.instance().get_klines(symbol=self.get_symbol(),date_a=date_a,date_b=date_b)
        for k in klines:
            loss = k.return_loss(self.get_stop_loss())
            profit = k.return_profit(self.get_sell())
            if (loss != CryptoFloat(self.get_symbol(),0)):
                self.set_loss(loss)
                self.set_profit(CryptoFloat.neutral_element(self.get_symbol()))
                BinanceExchange.instance().save_signal(self)
                return CryptoFloat(self.get_symbol(),loss)
            else:
                self.set_loss(CryptoFloat.neutral_element(self.get_symbol()))
                self.set_profit(profit)
                BinanceExchange.instance().save_signal(self)
                return CryptoFloat(self.get_symbol(),profit)
                
    
    def performance(self):
        
        # def price_inside_kline(current_kline):
        #     curr_value = CryptoFloat(current_kline.symbol,float(self.get_buy()))
        #     return (CryptoFloat(current_kline.symbol,curr_value) >= current_kline.low) and ( curr_value <= current_kline.high)
        
        try:
            d = Date(date_str=self.signal['timestampt'])
            symbol = Symbol(self.signal['symbol'])
            #klines = BinanceExchange.instance().get_klines(symbol=symbol,'')
            order_time_kline_format = d.parsed_date.strftime("%d %b, %Y")
            order_time_kline_format_after_two_days = (d.parsed_date + datetime.timedelta(days=1)).strftime("%d %b, %Y")
            Logger.log('checking signal date klines ' + symbol.uppercase_format())
            klines = BinanceExchange.instance().get_klines(symbol,order_time_kline_format,order_time_kline_format_after_two_days)
            buy_array = []
            for b in self.signal['buy']:
                try:
                    buy_array.append(CryptoFloat(symbol=symbol,float_value=float(b['numbers'][0])))
                except:
                    pass
                
                
            sell_array = []
            for s in self.signal['sell']:
                try:
                    sell_array.append(CryptoFloat(symbol=symbol,float_value=float(s['numbers'][0])))
                except:
                    pass
                
            buy_reached_kline = None
            sell_reached_kline = None
            
            i = 0
            time_to_profit = datetime.timedelta(minutes=0)
            start_price = buy_array[0]
            while buy_reached_kline==None and sell_reached_kline==None:
                if (klines[i].low > buy_array[0] or klines[i].high > buy_array[0]):
                    buy_reached_kline = klines[i]
                    sell_reached_kline = klines[i]
                    time_to_profit = time_to_profit + (sell_reached_kline.close_time - buy_reached_kline.opentime)
                i = i + 1
            end_price = klines[i].low
            aproximate_profit = sell_reached_kline.high - buy_array[0]
            profit_in_usdt = aproximate_profit.to_usdt().get_value()
            
            db = MongoConnector.get_instance()
            
            signal_performance = {}
            signal_performance['signal_id'] = self.signal['_id']
            signal_performance['timestampt'] = self.signal['timestampt']
            signal_performance['channel'] = self.signal['channel']
            signal_performance['symbol'] = self.get_symbol().uppercase_format() 
            signal_performance['aproximate_profit'] = aproximate_profit.get_value()
            signal_performance['time_to_profit_seconds'] = time_to_profit.seconds
            signal_performance['time_to_profit_microseconds'] = time_to_profit.microseconds
            signal_performance['start_price'] = start_price.get_value()
            signal_performance['end_price'] = end_price.get_value()
            signal_performance['start_price_usdt'] = start_price.to_usdt().get_value()
            signal_performance['end_price_usdt'] = end_price.to_usdt().get_value()
            signal_performance['aproximate_profit_usdt'] = profit_in_usdt
            signal_performance['percentage_profit'] = (100 / (start_price.get_value() / (end_price.get_value() - start_price.get_value())))
            
            try:
                db.insert_signal_performance(signal_performance)
                #print(str(self.signal['_id']) + "," +self.signal['timestampt'] + "," + self.signal['channel'] + "," +  self.get_symbol().uppercase_format() + "," + str(aproximate_profit) + "," + str(time_to_profit.seconds) + "," + str(time_to_profit.microseconds) + "," + str(profit_in_usdt))
                Logger.log('inserted_signal_performance: ' + str(signal_performance['signal_id']))
                return (aproximate_profit,time_to_profit)
            except:
                pass
            
        except:
            print('Ignoring problematic signal, continue with another...')
        
        
        
