from com_goldenthinker_trade_telegram.TelegramNotifier import TelegramNotifier
from com_goldenthinker_trade_monitor.Ticker import Ticker
from com_goldenthinker_trade_utils.Date import Date
from com_goldenthinker_trade_datatype.CryptoFloat import CryptoFloat
from com_goldenthinker_trade_model.Symbol import Symbol

import prettytable as pt


import time

ticker = Ticker.instance()



leveraged_tokens = ['1INCHUP','1INCHDOWN','XLMDOWN','XLMUP','SUSHIDOWN','SUSHIUP','AAVEDOWN','AAVEUP','BHCDOWN','BHCUP','YFIDOWN','YFIUP','FILDOWN','FILUP','SXPDOWN','SXPUP','UNIDOWN','UNIUP','LTCDOWN','LTCUP','XRPDOWN','XRPUP','DOTDOWN','DOTUP','TRXDOWN','TRXUP','EOSDOWN','EOSUP','XTZDOWN','XTZUP','BNBDOWN','BNBUP','LINKDOWN','LINKUP','ADADOWN','ADAUP','ETHDOWN','ETHUP','BTCDOWN','BTCUP']
crypto_tokens = ['1INCH','XLM','SUSHI','AAVE','BHC','YFI','FIL','SXP','UNI','LTC','XRP','DOT','TRX','EOS','XTZ','BNB','LINK','ADA','ETH','BTC']


def crypto_token_tickers():
    tickers_all_currencies = ticker.get_all_tickers()
    return {k:v for k,v in tickers_all_currencies.items()}


telegram = TelegramNotifier.get_instance()
start_time = Date().now()
current_time = Date().now()

while True:
    
    tickers = crypto_token_tickers()
    
    ups_per_symbol = dict()
    [ups_per_symbol.__setitem__(x,0) for x in tickers]
    downs_per_symbol = dict()
    [downs_per_symbol.__setitem__(x,0) for x in tickers]
    delta_per_symbol = dict()
    [delta_per_symbol.__setitem__(x,0) for x in tickers]
    delta_percentage = dict()
    [delta_percentage.__setitem__(x,0) for x in tickers]
    total_earning_for_symbol = dict()
    [total_earning_for_symbol.__setitem__(x,0) for x in tickers]
    
    
    while (Date().time_difference_in_min(start_time,current_time) <= 15):
        tickers_old = tickers
        time.sleep(30)
        tickers = crypto_token_tickers()
        for k in tickers.keys():
            delta = float(tickers[k])-float(tickers_old[k])
            total_earning_for_symbol[k] = total_earning_for_symbol[k] + delta
            if (delta<0):
                ups_per_symbol[k] = ups_per_symbol[k] + 1
            else:
                downs_per_symbol[k] = downs_per_symbol[k] + 1
            delta_per_symbol[k] = delta_per_symbol[k] + delta
            delta_percentage[k] = delta_percentage[k] + ( ((delta/100)*tickers[k]) - ((delta/100)*tickers_old[k]) )
        
        current_time = Date().now()
        
    total_earning_for_symbol_sorted_by_highest_value = dict(sorted(total_earning_for_symbol.items(), key=lambda x:x[1],reverse=True))
    total_earning_for_symbol_sorted_by_lowest_value = dict(sorted(total_earning_for_symbol.items(), key=lambda x:x[1]))

    ups_per_symbol_sorted = dict(sorted(ups_per_symbol.items(), key=lambda x:x[1],reverse=True))
    downs_per_symbol_sorted = dict(sorted(downs_per_symbol.items(), key=lambda x:x[1],reverse=True))
    
    delta_sorted_by_lowest_value = dict(sorted(delta_per_symbol.items(), key=lambda x:x[1]))
    delta_sorted_by_highest_value = dict(sorted(delta_per_symbol.items(), key=lambda x:x[1],reverse=True))
    
    delta_percentage_by_lowest_value = dict(sorted(delta_percentage.items(), key=lambda x:x[1]))
    delta_percentage_by_highest_value = dict(sorted(delta_percentage.items(), key=lambda x:x[1],reverse=True))
    
    
    table_header = pt.PrettyTable(['Symbol','Max_Earning','Symbol_a','Max_Rises','Symbol_b','MaxDelta %'])
    table_header.align['Symbol'] = 'l'
    table_header.align['Max_Earning'] = 'r'
    table_header.align['Symbol_a'] = 'r'
    table_header.align['Max_Rises'] = 'r'
    table_header.align['Symbol_b'] = 'r'
    table_header.align['MaxDelta %'] = 'r'
    
    
    data = list(zip(list(total_earning_for_symbol_sorted_by_highest_value),list(total_earning_for_symbol_sorted_by_highest_value.values()),list(ups_per_symbol_sorted),list(ups_per_symbol_sorted.values()),list(delta_percentage_by_highest_value),list(delta_percentage_by_highest_value.values())))[0:30]
    

    for symbol, max_earning, symbol_a, max_rises, symbol_b, max_delta_percent in data:
        table_header.add_row([symbol, f'{max_earning:.8f}', symbol_a, f'{max_rises:.8f}', symbol_b,f'{max_delta_percent:.8f}' ])
    
        
    message = f'<pre>{table_header}</pre>'
    message_chunks = [message[i:i+4096] for i in range(0, len(message), 4096)]
    for chunk in message_chunks:
        time.sleep(2)
        telegram.send_message(message=chunk)
    
    
    
    table_header_low = pt.PrettyTable(['Symbol','Min_Earning','Symbol_a','Max_Drops','Symbol_b','MinDelta %'])
    table_header_low.align['Symbol'] = 'l'
    table_header_low.align['Min_Earning'] = 'r'
    table_header_low.align['Symbol_a'] = 'r'
    table_header_low.align['Max_Drops'] = 'r'
    table_header_low.align['Symbol_b'] = 'r'
    table_header_low.align['MinDelta %'] = 'r'
    
    
    data = list(zip(list(total_earning_for_symbol_sorted_by_lowest_value),list(total_earning_for_symbol_sorted_by_lowest_value.values()),list(downs_per_symbol_sorted),list(downs_per_symbol_sorted.values()),list(delta_percentage_by_lowest_value),list(delta_percentage_by_lowest_value.values())))[0:30]
    

    for symbol, min_earning, symbol_a, max_drops, symbol_b, min_delta_percent in data:
        table_header_low.add_row([symbol, f'{min_earning:.8f}', symbol_a, f'{max_drops:.8f}', symbol_b,f'{min_delta_percent:.8f}' ])
    
    
        
    message = f'<pre>{table_header_low}</pre>'
    message_chunks = [message[i:i+4096] for i in range(0, len(message), 4096)]
    for chunk in message_chunks:
        time.sleep(2)
        telegram.send_message(message=chunk) 


        
    start_time = current_time
    current_time = Date().now()