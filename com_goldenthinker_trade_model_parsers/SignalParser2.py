import re
import sys

if 'com_goldenthinker_trade_model_signals.BuySellSignal' not in sys.modules:
    from com_goldenthinker_trade_model_signals.BuySellSignal import BuySellSignal
if 'com_goldenthinker_trade_model_signals.BuySignal' not in sys.modules:
    from com_goldenthinker_trade_model_signals.BuySignal import BuySignal
if 'com_goldenthinker_trade_model_signals.SellSignal' not in sys.modules:
    from com_goldenthinker_trade_model_signals.SellSignal import SellSignal
    
from dateutil.parser import ParserError, parse
from com_goldenthinker_trade_utils.Date import Date


class SignalParser2:
    
    def __init__(self, unstructred_text=None,timestampt=None,channel=None):
        self.unstructured_text = unstructred_text
        self.timestampt = timestampt
        self.channel = channel
        
    def parse(self):
        sinonyms_dict = {
            "buy": ["buy","entry","entryzone","entry zone","buy around"],
            "sell": ["sell","target","goal","exit","profit"],
            "stoploss": ["stoploss","stop loss","loss","stop"],
            "price": ["current","current ask"],
            "volume": ["volume"],
            "exchange": ["at"]
        }
        
        options_dict = {
            "account": ["spot","features"],
            "strategy":["short","long"],
            "account": ["spot","futures"],
            "exchange": ["binance","huobi global","coinbase","kraken","bithumb","bitfinex","bitstamp","ftx","bitflyer","bitrex","huobi"]
        }
        
        def parse_signal(signal):
            
            s = {}
            remove_links = re.sub(r'http\S+', '', signal)
            signal_clean = re.sub("[^\w:( )\n\.-]", "", remove_links).lower()
            signal = signal_clean
            
            def keywords_values_per_line(signal):
                separate_in_lines = signal.split('\n')
                lines = []
                for each_line in separate_in_lines:
                    my_line = each_line
                    if (each_line!=''):
                        date_in_line = []
                        try:
                            parsed_date = parse(each_line,fuzzy_with_tokens=True)
                            date_in_line.append(parsed_date[0]) # extracts date
                            each_line = ' '.join(parsed_date[1])
                        except ParserError:
                            pass
                        except OverflowError:
                            pass
                        
                        percentages = re.findall(r"\d*?.\d*%", each_line)
                        
                        for p in percentages:
                            signal_percentage_removed = each_line.replace(p,'')
                            each_line = signal_percentage_removed
                                                
                        numbers = re.findall(r"[-+]?\d*\.\d+|\d+", each_line)
                        for n in numbers:
                            signal_number_removed = each_line.replace(n,'')
                            each_line = signal_number_removed
                        
                        words_in_signal_line = re.findall(r"([a-zA-Z]+)", each_line)
                        
                        for w in words_in_signal_line:
                            signal_word_removed = each_line.replace(w,'')
                            each_line = signal_word_removed
                            
                        
                        line_components = { 'date_in_line' : Date().serialize(date_in_line),
                                            'percentages' : percentages,
                                            'numbers' : numbers,
                                            'words_in_signal_line' : words_in_signal_line,
                                            'raw_line': my_line }

                        lines.append(line_components)    
                #print("ResultingSignalText: " + str(lines))
                return lines
            
            
            def get_symbol(signal_line):
                with open("com_goldenthinker_trade_telegram/symbols.txt") as f:
                    symbols_upper_case = f.readlines()
                symbols = [s.lower().replace('\n','') for s in symbols_upper_case]
                for si in symbols:
                    s_a = si.split("/")[0]
                    s_b = si.split("/")[1]
                    lower_case_signal_line = [x.lower() for x  in signal_line]
                    symbols_present_in_line = s_a in lower_case_signal_line and s_b in lower_case_signal_line
                    if not symbols_present_in_line:
                        symbols_present_in_line = re.search(s_a+".{0,6}"+s_b,'/'.join(lower_case_signal_line))
                        if symbols_present_in_line==None:
                            symbols_present_in_line = False
                        else:
                            symbols_present_in_line = True
                    if symbols_present_in_line:
                        s['symbol'] = si
                        s['symbol_a'] = s_a
                        s['symbol_b'] = s_b
                        return True            
                return False
                
            parsed_lines = keywords_values_per_line(signal)
                        
            for i,line in enumerate(parsed_lines):
                if get_symbol(line['words_in_signal_line']):
                    break
                
            for line in parsed_lines:   
                
                for key in sinonyms_dict:
                    for keyword_horizontal in sinonyms_dict[key]:
                        for w in line['words_in_signal_line']:
                            if w.lower() == keyword_horizontal:
                                if s.get(key)==None:
                                    s[key] = []
                                s[key].append(line)
                                break
                            break
                                
                for key in options_dict:
                    for keyword_horizontal in options_dict[key]:
                        for w in line['words_in_signal_line']:
                            if w.lower() == keyword_horizontal:
                                if s.get(key)==None:
                                    s[key] = []
                                line['words_in_signal_line'] = w.lower()
                                s[key].append(line)
                                
                                
            if s.get('symbol')!=None:
                if (s.get('buy')!=None and s.get('sell')!=None):
                    return BuySellSignal(signal_dict=s,when_signal_ocurred=self.timestampt,channel_name=self.channel)
                else:
                    if s.get('buy')!=None:
                        return BuySignal(signal_dict=s,when_signal_ocurred=self.timestampt,channel_name=self.channel)
                    else:
                        if s.get('sell')!=None:
                            return SellSignal(signal_dict=s,when_signal_ocurred=self.timestampt,channel_name=self.channel) 
                        else:
                            print('InvalidSignal: ' + str(s))    
                            return None
            else:
                print('InvalidSignal: ' + str(s))    
                return None
            
        return parse_signal(self.unstructured_text)
