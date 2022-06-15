from com_goldenthinker_trade_utils.Utils import Utils
from datetime import datetime
from com_goldenthinker_trade_model.Signal import Signal

from com_goldenthinker_trade_sessions.BinanceSession import BinanceSession
from com_goldenthinker_trade_sessions.TinyDbSession import TinyDbSession

from binance.exceptions import BinanceAPIException
from binance.client import Client

from tinydb import Query
from tinydb.database import TinyDB

import datetime
from dateutil.parser import parse


class PerformanceCalculator:
    def __init__(self):
        pass
    
    def calculate_signals_perfornance(self):
        binance_client = BinanceSession().client
        
        db = TinyDB('com_goldenthinker_trade_model/signals.json')

        user = Query()
        signals = db.all()

        # Prepare CSV file

        now = datetime.datetime.now()
        current_date = now.strftime("%Y_%m_%d")
        logfile_path = "report_signals-" + current_date + ".csv"
        
        def line_prepender(filename, line):
            with open(filename, 'r+') as f:
                content = f.read()
                f.seek(0, 0)
                f.write(line.rstrip('\r\n') + '\n' + content)
                

        def calculate_margin_for(signal,kline):
            
            def valid_float(my_float):
                try:
                    float(my_float)
                    return True
                except ValueError:
                    return False

            try:
                
                margin = 0
                time_to_margin = 0
                # The format of bitcoin amounts in some signals are just four numbers like 4532 difficultingt the
                # processing of the signalks, so the following multiplicator if the symbol is XXX/BTC the multiplicator is then 10**-6 0.004532
            
                s = Signal(signal_dict=signal)
                
                info = binance_client.get_symbol_info(symbol=signal['symbol'])
                
                
                multiplicator = 1
                if ('/btc' in s.signal['symbol']) and ('.' in kline[1]):   # if BTC expressed without leading 0s as four numbers we add 0.00 later by using the multiplicator
                    multiplicator = 10**-6

                kline_date = (datetime.datetime.fromtimestamp(int(kline[0])/1000)).replace(tzinfo=None)
                signal_date = parse(s.signal['timestampt']).replace(tzinfo=None)
                signal_date_10_days = (signal_date + datetime.timedelta(days=10)).replace(tzinfo=None)
                time_to_margin = kline_date - signal_date
                
                # check that the kline is within the signal timestampt and no more than 10 days
                if (kline_date >= signal_date) and (kline_date <= signal_date_10_days):
                        
                    # checks if the current kline triggered the signal and if it reached stoploss 
                    # returns negative margin and if the target was reached returns the margin earned
                    try:
                        entry = s.signal[s.to_array()[0]]
                        target = s.signal[s.to_array()[1]]
                        stop = s.signal[s.to_array()[2]]
                        
                        if valid_float(kline[1]) and valid_float(entry) and valid_float(target) and valid_float(stop):
                        
                            a = (float(kline[1]) >= Utils().precision(signal['symbol'],float(entry)))
                            b = (float(kline[1]) >= Utils().precision(signal['symbol'],float(target)))
                            c = (float(kline[1]) > Utils().precision(signal['symbol'],float(stop)))
                            
                            if (a and b and c):
                                
                                # if stop loss has not reached before it will check if the current kline reached the target
                                for i in range(1,5):
                                    #  check if a target was reached and calculate margin
                                    if float(kline[i]) >= (float(target)*multiplicator):
                                        margin = float(kline[i]) - (float(entry)*multiplicator)
                                        return (margin,kline_date,time_to_margin)
                                                    
                                for i in range(1,5):
                                    # if this kline reached the stop loss generating it generates the negative margin
                                    # in any of the values of the Open, Hign, Low, Close of the kline
                                    if float(kline[i]) <= (float(stop)*multiplicator):
                                        margin = float(kline[i]) - (float(entry)*multiplicator)
                                        return (margin,kline_date,time_to_margin)

                                #if no stoploss has been triggered and no target has been triggered then the returned margin will be 0
                                return (0,kline_date,0)
                            else:
                                # if the signal was not triggered by this kline then there is no margin for this kline
                                return (margin,kline_date,time_to_margin)
                        else:
                            (0,kline_date,0)
                    except TypeError:
                        print("The signal " + str(s.signal['id']) + " has problems with the field names.")
                        return (0,kline_date,0)
                    except KeyError:
                        print("The signal " + str(s.signal['id']) + " has problems with the field names.")
                        return (0,kline_date,0)
                else:
                    # if the kline is not for the current signal then there is no margin
                    return (0,kline_date,0)
            except TypeError:
                print("Signal is not valid ")
                return (0,0,0)


        # For each signal retrieve all klines from the time of the signal to 10 days and format date 
        # in order to obtain all klines during the period using a 30 min interval each

        for each_signal in signals:
            signal_date = parse(each_signal['timestampt'])
            signal_date_10_days = signal_date + datetime.timedelta(days=10)
            formatted_signal_date = signal_date.strftime("%d %b, %Y")
            formatted_signal_date_10_days = signal_date_10_days.strftime("%d %b, %Y")
            
            # Obtain all klines from Binance API for the signal date on 10 days
            try:
                klines = binance_client.get_historical_klines(''.join(each_signal['symbol'].split('/')).upper(), Client.KLINE_INTERVAL_30MINUTE, formatted_signal_date, formatted_signal_date_10_days)
            
                for each_kline in klines:
                    margin , kline_date, time_to_margin = calculate_margin_for(each_signal,each_kline)
                    if margin != 0:
                        days, seconds = time_to_margin.days, time_to_margin.seconds
                        hours = days * 24 + seconds // 3600
                        minutes = (seconds % 3600) // 60
                        seconds = seconds % 60
                        with open(logfile_path, "a+") as log_file:
                            current_log_line = str(each_signal['id']) + "," + each_signal['symbol'] + "," + str(each_signal['timestampt']) + "," + str(kline_date) + ","+ str(time_to_margin).replace(",",'_') + "," + str(time_to_margin.days) + "," + str(hours) + "," + str(minutes)+ "," + str(seconds) + "," + str(margin) + "\n"
                            print(current_log_line)
                            log_file.write(current_log_line)
                        break
            except BinanceAPIException:
                try:
                    print("Symbol " + str(each_signal['symbol']) + " is not supported in " + str(each_signal['exchange']) + " exchange." )
                except KeyError:
                    print("Symbol " + str(each_signal['symbol']) + " is not supported in exchange.")
                    
                    
        line_prepender(logfile_path,('id' + "," + 'symbol' + "," + 'timestampt' + "," + 'kline_date' + ","+ "time_to_margin" + "," + "margin_time_days" + "," + "margin_time_hours" + "," + "margin_time_minutes" + "," + "margin_time_seconds" + "," + "margin_amount" + "\n") )
        return "Check log " + logfile_path