import re

signal_0 = """Open long

Lev 10 , 20, 30 ,40, 50%

Eth/USDT 

2442 Buy Around    
                                                                                                                                                                                                                                                                                                                                 
2200 STOP LOSs

Target 1   2490

Target 2   2530
Target 3    2580++++"""

signal_1 = """🦹 Hey Golden, I've registered a new signal for ANKRBTC provided by the pro trader Quality Signals Free

• 🐮 Strategy: Long
• 👉 Exchange: BINANCE
• 👉 Account: Spot
• 👉 Invest: 2%
• 🎯 Exit:
• ⎿  Target 3 : 238  12.26%
• ⎿  Target 2 : 234  10.38%
• ⎿  Target 1 : 231  8.96%
• 💰 Entry: 205 ⌁ 219
• ⎿  Current market price: 218
• 🚫 Stop: 201 (-5.19%) 

• 📊 Technical indicators:
•  ⎿  24h Volume: 45.4964665
•  ⎿  Satoshis: 218
•  ⎿  Analysis: TradingView"""


signal_2 = """✳ New FREE signal

💎 Buy #ABT/#BTC at #HUOBI

🆔 #837553, 10th today.
⏱ 10-Jun-2021 22:33:38 UTC

🛒 Entry Zone: 0.00000304 - 0.00000327
💵 Current ask: 0.00000327 
🎯 Target 1: 0.0000034 (3.98%)
🎯 Target 2: 0.00000346 (5.81%)
🎯 Target 3: 0.00000351 (7.34%)
🚫 Stop loss: 0.00000297 (9.17%)
💰 Volume #ABT: 260,848.8
💰 Volume #BTC: 0.89

⏳ SHORT TERM (up to 7 days)
⚠️ Risk: 3/5 (Medium) - Invest up to 5% of your portfolio
☯️ R/R ratio: 1:0.6️

ArcBlock (ABT) | Overview | Chart"""


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
    signal_clean = re.sub("[^\w:( )\n\.-]", "", signal).lower()
    signal = signal_clean
    
    def keywords_values_per_line(signal):
        separate_in_lines = signal.split('\n')
        lines = []
        for each_line in separate_in_lines:
            if (each_line!=''):
                numbers = re.findall(r"[-+]?\d*\.\d+|\d+", each_line)
                words_in_signal_line = re.findall(r"([a-zA-Z]+)", each_line)
                percentages = re.findall(r"\d*?.\d*%", each_line)
                for n in numbers:
                    signal_number_removed = signal.replace(n,'')
                    signal = signal_number_removed
                for w in words_in_signal_line:
                    signal_word_removed = signal.replace(w,'')
                    signal = signal_word_removed
                for p in percentages:
                    signal_percentage_removed = signal.replace(p,'')
                    signal = signal_percentage_removed
                lines.append((words_in_signal_line,numbers,percentages))    
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
        if get_symbol(line[0]):
            break
    
    
    
    for line in parsed_lines:   
        
        for key in sinonyms_dict:
            for keyword_horizontal in sinonyms_dict[key]:
                for w in line[0]:
                    if w.lower() == keyword_horizontal:
                        if s.get(key)==None:
                            s[key] = []
                        s[key].append(line[0])
                        s[key].append(line[1])
                        s[key].append(line[2])
                        break
                    break
                        
        for key in options_dict:
            for keyword_horizontal in options_dict[key]:
                for w in line[0]:
                    if w.lower() == keyword_horizontal:
                        if s.get(key)==None:
                            s[key] = []
                        s[key].append(w.lower())
                        s[key].append(line[1])
                        s[key].append(line[2])
    
    
                    
    if s.get('symbol')!=None and s.get('buy')!=None and s.get('sell')!=None and s.get('stoploss')!=None:
        print(str(s))
        return s
    else:
        print('InvalidSignal: ' + str(s))    
        return None                            
    
        
        
parse_signal(signal_1)
