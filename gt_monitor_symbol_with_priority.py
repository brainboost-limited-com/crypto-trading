from datetime import datetime, timedelta,timezone

from com_goldenthinker_trade_datasource_network.TickerSocketMultipleSymbols import TickerSocketMultipleSymbols
from com_goldenthinker_trade_exchange.ExchangeConfiguration import ExchangeConfiguration
from com_goldenthinker_trade_logger.Logger import Logger
import datetime
import os
from threading import Thread





Logger.set_process_name = 'gt_monitor_symbol_with_priority'


def update_symbols():
        with open("priority_symbols.list", 'r') as f:

                symbols_to_monitor = f.read().replace('\n','').split(',')
                while symbols_to_monitor != '':
                        open('priority_symbols.list', 'w').close()
                symbols_to_monitor = f.read().replace('\n','').split(',')
                return symbols_to_monitor

def start_symbol_monitors(symbols_to_monitor):
        my_ticker_socket = TickerSocketMultipleSymbols(exchange=ExchangeConfiguration.get_default_exchange(),symbols=symbols_to_monitor)
        my_ticker_socket.start()


filename = "priority_symbols.list"
statbuf = os.stat(filename)
last_time_symbols_list_updated = statbuf.st_mtime



while True:
        
        while datetime.datetime.fromtimestamp(last_time_symbols_list_updated) < (datetime.datetime.now()-timedelta(seconds=10)):
                statbuf = os.stat(filename)
                last_time_symbols_list_updated = statbuf.st_mtime
        symbols_to_monitor = update_symbols()
        t = Thread(target=start_symbol_monitors, args=(symbols_to_monitor,))     
        t.start()
# Once an order is created from the robot.py script,
# then the symbols are monitored in case the current price goes below expected



    










