import re
from com_goldenthinker_trade_model.Symbol import Symbol

class SignalParserOld:
    
    def __init__(self,unstructured_text):
        self.unstructured_text = unstructured_text 
    
    def parse(self):
        self.signal_unstructured_text_clean = re.sub("[^\w:( )\n\.-]", "", self.unstructured_text).lower()
        self.signal = dict()

        
        def get_symbol(signal_text):
            with open("com_goldenthinker_trade_telegram/symbols.txt") as f:
                symbols_upper_case = f.readlines()
            symbols = [Symbol(s.lower().replace('\n','')) for s in symbols_upper_case]
            for s in symbols:
                s_a = s.symbol_a()
                s_b = s.symbol_b()
                symbol_present = (s in signal_text) or (s.replace('/','') in signal_text) or ((s_a in signal_text) and (s_b in signal_text))
                if symbol_present:
                    self.signal['symbol'] = s.lowercase_format_slashed()
                    self.signal['symbol_a'] = s_a
                    self.signal['symbol_b'] = s_b
                    self.signal['id'] = hash(str(self.signal['symbol']) + str(self.signal['timestampt']))    
                    break
                                
        def get_exchange(signal_text):
            exchanges = ["binance","huobi global","coinbase","kraken","bithumb","bitfinex","bitstamp","ftx","bitflyer","bitrex"]
            couunt_exchanges_mentioned = 0
            for e in exchanges:
                if e in signal_text:
                    couunt_exchanges_mentioned = couunt_exchanges_mentioned + 1
                    self.signal['exchange'] = e
                    break
                        
        def get_signal_fields(signal_text):
            lines = signal_text.split('\n')
            lines_with_double_dots = [l for l in lines if (':' in l)]
            lines_with_double_dots_and_no_minus_in_the_value_field = [x for x in lines_with_double_dots if ('-' not in x.split(':')[1])]
            for l in lines_with_double_dots_and_no_minus_in_the_value_field:
                l_a = l.split(':')[0]
                l_b = l.split(':')[1]
                if (' ' in l_b):
                    value_elements = [x for x in (l_b.split(' ')) if x != '']
                    for i,v in enumerate(value_elements):
                        self.signal[l_a.replace(' ',"") + "_" + str(i)] = v.replace(' ','')
                else:
                    self.signal[l_a.replace(' ',"")] = l_b.replace(' ','')
            lines_with_double_dots_and_minus_in_the_value_field = [x for x in lines_with_double_dots if ('-' in x.split(':')[1])]
            for l in lines_with_double_dots_and_minus_in_the_value_field:
                l_a = l.split(':')[0]
                l_b = l.split(':')[1]
                if ('-' in l_b):
                    value_elements = [x for x in (l_b.split('-')) if x != '']
                    for i,v in enumerate(value_elements):
                        self.signal[l_a.replace(' ',"") + "_" + str(i)] = v.replace(' ','')
                else:
                    self.signal[l_a.replace(' ',"")] = l_b.replace(' ','')
                
                
        
        self.find_elements_in_signal = [get_symbol,get_exchange,get_signal_fields]
        
        for f in self.find_elements_in_signal:
            f(self.signal_unstructured_text_clean)
            
        if self.valid()==False:
            raise TypeError
        