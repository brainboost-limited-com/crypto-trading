import re
from abc import abstractmethod
from dataclasses import replace
from datetime import datetime

from telethon import TelegramClient, events

api_id = 3820623
api_hash = 'de74cd9776235755c03d27cc0d4b1507'


datetimeObject = datetime.now()
session_str = "session_telegram_" + datetimeObject.strftime('%Y%m%d%H%M%S')
print("SESSION: "+session_str)
client = TelegramClient(session_str, api_id, api_hash)

#@client.on(events.NewMessage(chats="@Crypto_Binance_Trading"))

event_markup = dict()


class SignalMockup:
    def __init__(self,signal_data_dic):
        self.data = signal_data_dic
        self.symbol = self.data['symbol']
        self.symbol_a = self.data['symbol_a']
        self.symbol_b = self.data['symbol_b']
        self.exchange = self.data['exchange']
        self.time = self.data['time']
        self.entry_zone_a = self.data['entry_zone_a']
        self.entry_zone_b = self.data['entry_zone_b']
        self.current_ask = self.data['current_ask']
        self.target_1 = self.data['target_1']
        self.target_2 = self.data['target_2']
        self.target_3 = self.data['target_3']
        self.stoploss = self.data['stoploss']
        self.volume_symbol_a = self.data['volume_symbol_a']
        self.volume_symbol_b = self.data['volume_symbol_b']
        self.rsi = self.data['rsi']
    
    
        
        
    def __str__(self):
        return str(self.data)
    
    def execute(self):
        pass



@client.on(events.NewMessage(incoming=True,chats=['@AnnyDeCrypto_bot']))
async def my_event_handler(event):
    ts = str(datetimeObject.strftime('%Y%m%d%H%M%S'))
    event_markup["ts"] = ts
    event_markup["message"] = event.text  
    print('filtered by channel user name: AnnyDeCrypto_bot ')
    print(event.text)
    def parse(signal_text):
        print("Procesing signal: ")
        #signal_text_filtered =  re.sub('([A-Z]{6,8})|\w+.*:.*',signal_text)
        if (re.search("(.*)registered a new signal(.*)((([A-Z]|[0-9]){0,5}BTC)|(([A-Z]|[0-9]){0,5}USDT))(.*)", signal_text)!=None):
            print("CQSFreeCornix buy signal detected..")
            signal = dict()
            lines = signal_text.split('\n')
            signal['symbol'] = lines[2].split("#")[1][0:-1] + "/" + lines[2].split("#")[2].split(' ')[0]
            signal['symbol_a'] = lines[2].split("#")[1][0:-1]
            signal['symbol_b'] = lines[2].split("#")[2].split(' ')[0]
            signal['exchange'] = lines[2].split("#")[3]
            signal['time'] = lines[5]
            signal['entry_zone_a'] = (lines[7].split(":")[1].split('-')[0]).replace(" ", "")
            signal['entry_zone_b'] = (lines[7].split(":")[1].split('-')[1]).replace(" ", "")
            signal['current_ask'] =  lines[8].split(":")[1].replace(" ","")
            signal['target_1'] = lines[9].split(":")[1].split(" ")[1]
            signal['target_2'] = lines[10].split(":")[1].split(" ")[1]
            signal['target_3'] = lines[11].split(":")[1].split(" ")[1]
            signal['stoploss'] = lines[12].split(":")[1].split(" ")[1]
            signal['volume_symbol_a'] = lines[13].split(":")[1].replace(" ","")
            signal['volume_symbol_b'] = lines[14].split(":")[1].replace(" ","")
            signal['rsi'] = lines[15].split(":")[1].replace(" ","")
            return SignalMockup(signal)
        else:
            print("This was not a signal...")
            
    parsed_signal = parse(event.text)
    print(str(parsed_signal))
    

    
@client.on(events.NewMessage(incoming=True,chats=['@cryptosignalsMaverick']))
async def my_event_handler(event):
    ts = str(datetimeObject.strftime('%Y%m%d%H%M%S'))
    event_markup["ts"] = ts
    event_markup["message"] = event.text  
    print('filtered by channel user name: cryptosignalsMaverick ')
    print(event.text)
    def parse(signal_text):
        print("Procesing signal: ")
        #signal_text_filtered =  re.sub('([A-Z]{6,8})|\w+.*:.*',signal_text)
        if (re.search("(.*)(([A-Z]|[0-9]){0,5}/BTC)|(([A-Z]|[0-9]){0,5}/USDT)(.*)", signal_text)!=None):
            print("CQSFreeCornix buy signal detected..")
            signal = dict()
            lines = signal_text.split('\n')
            signal['symbol'] = lines[2].split("#")[1][0:-1] + "/" + lines[2].split("#")[2].split(' ')[0]
            signal['symbol_a'] = lines[2].split("#")[1][0:-1]
            signal['symbol_b'] = lines[2].split("#")[2].split(' ')[0]
            signal['exchange'] = lines[2].split("#")[3]
            signal['time'] = lines[5]
            signal['entry_zone_a'] = (lines[7].split(":")[1].split('-')[0]).replace(" ", "")
            signal['entry_zone_b'] = (lines[7].split(":")[1].split('-')[1]).replace(" ", "")
            signal['current_ask'] =  lines[8].split(":")[1].replace(" ","")
            signal['target_1'] = lines[9].split(":")[1].split(" ")[1]
            signal['target_2'] = lines[10].split(":")[1].split(" ")[1]
            signal['target_3'] = lines[11].split(":")[1].split(" ")[1]
            signal['stoploss'] = lines[12].split(":")[1].split(" ")[1]
            signal['volume_symbol_a'] = lines[13].split(":")[1].replace(" ","")
            signal['volume_symbol_b'] = lines[14].split(":")[1].replace(" ","")
            signal['rsi'] = lines[15].split(":")[1].replace(" ","")
            return SignalMockup(signal)
        else:
            print("This was not a signal...")
            
                
    parsed_signal = parse(event.text)
    print(str(parsed_signal))
    
    
    
    
    
    
    
@client.on(events.NewMessage(incoming=True,chats=['@CQSFreeCornix']))
async def my_event_handler(event):
    ts = str(datetimeObject.strftime('%Y%m%d%H%M%S'))
    event_markup["ts"] = ts
    event_markup["message"] = event.text
    print('filtered by channel user name: CQSFreeCornix ')
    print(event.text)
    
    def parse(signal_text):
        print("Procesing signal: ")
        #signal_text_filtered =  re.sub('([A-Z]{6,8})|\w+.*:.*',signal_text)
        if (re.search("(.*)Buy #([A-Z]{0,5})/#([A-Z]{0,5})(.*)", signal_text)!=None):
            print("CQSFreeCornix buy signal detected..")
            signal = dict()
            lines = signal_text.split('\n')
            signal['symbol'] = lines[2].split("#")[1][0:-1] + "/" + lines[2].split("#")[2].split(' ')[0]
            signal['symbol_a'] = lines[2].split("#")[1][0:-1]
            signal['symbol_b'] = lines[2].split("#")[2].split(' ')[0]
            signal['exchange'] = lines[2].split("#")[3]
            signal['time'] = lines[5]
            signal['entry_zone_a'] = (lines[7].split(":")[1].split('-')[0]).replace(" ", "")
            signal['entry_zone_b'] = (lines[7].split(":")[1].split('-')[1]).replace(" ", "")
            signal['current_ask'] =  lines[8].split(":")[1].replace(" ","")
            signal['target_1'] = lines[9].split(":")[1].split(" ")[1]
            signal['target_2'] = lines[10].split(":")[1].split(" ")[1]
            signal['target_3'] = lines[11].split(":")[1].split(" ")[1]
            signal['stoploss'] = lines[12].split(":")[1].split(" ")[1]
            signal['rsi'] = lines[13].split(":")[1].replace(" ","")
            return SignalMockup(signal)
        else:
            print("This was not a signal...")
    
    parsed_signal = parse(event.text)
    print(str(parsed_signal))
    
    
    
    
    
@client.on(events.NewMessage(incoming=True,chats=['@cryptosignalsMaverick']))
async def my_event_handler(event):
    ts = str(datetimeObject.strftime('%Y%m%d%H%M%S'))
    event_markup["ts"] = ts
    event_markup["message"] = event.text  
    print(event.text)
    def parse(signal_text):
        print("Procesing signal: ")
        #signal_text_filtered =  re.sub('([A-Z]{6,8})|\w+.*:.*',signal_text)
        if (re.search("(.*)Buy #([A-Z]{0,5})/#([A-Z]{0,5})(.*)", signal_text)!=None):
            print("CQSFreeCornix buy signal detected..")
            signal = dict()
            lines = signal_text.split('\n')
            signal['symbol'] = lines[2].split("#")[1][0:-1] + "/" + lines[2].split("#")[2].split(' ')[0]
            signal['symbol_a'] = lines[2].split("#")[1][0:-1]
            signal['symbol_b'] = lines[2].split("#")[2].split(' ')[0]
            signal['exchange'] = lines[2].split("#")[3]
            signal['time'] = lines[5]
            signal['entry_zone_a'] = (lines[7].split(":")[1].split('-')[0]).replace(" ", "")
            signal['entry_zone_b'] = (lines[7].split(":")[1].split('-')[1]).replace(" ", "")
            signal['current_ask'] =  lines[8].split(":")[1].replace(" ","")
            signal['target_1'] = lines[9].split(":")[1].split(" ")[1]
            signal['target_2'] = lines[10].split(":")[1].split(" ")[1]
            signal['target_3'] = lines[11].split(":")[1].split(" ")[1]
            signal['stoploss'] = lines[12].split(":")[1].split(" ")[1]
            signal['volume_symbol_a'] = lines[13].split(":")[1].replace(" ","")
            signal['volume_symbol_b'] = lines[14].split(":")[1].replace(" ","")
            signal['rsi'] = lines[15].split(":")[1].replace(" ","")
            return SignalMockup(signal)
        else:
            print("This was not a signal...")
            
                
    parsed_signal = parse(event.text)
    print(str(parsed_signal))
    
    
    
    
    
@client.on(events.NewMessage(incoming=True,chats=['@QualitySignalsChannel']))
async def my_event_handler(event):
    ts = str(datetimeObject.strftime('%Y%m%d%H%M%S'))
    event_markup["ts"] = ts
    event_markup["message"] = event.text
    print('filtered by channel user name: QualitySignalsChannel ')
    print(event.text)
    
    def parse(signal_text):
        print("Procesing signal: ")
        #signal_text_filtered =  re.sub('([A-Z]{6,8})|\w+.*:.*',signal_text)
        if (re.search("(.*)Buy #([A-Z]{0,5})/#([A-Z]{0,5})(.*)", signal_text)!=None):
            print("CQSFreeCornix buy signal detected..")
            signal = dict()
            lines = signal_text.split('\n')
            signal['symbol'] = lines[2].split("#")[1][0:-1] + "/" + lines[2].split("#")[2].split(' ')[0]
            signal['symbol_a'] = lines[2].split("#")[1][0:-1]
            signal['symbol_b'] = lines[2].split("#")[2].split(' ')[0]
            signal['exchange'] = lines[2].split("#")[3]
            signal['time'] = lines[5]
            signal['entry_zone_a'] = (lines[7].split(":")[1].split('-')[0]).replace(" ", "")
            signal['entry_zone_b'] = (lines[7].split(":")[1].split('-')[1]).replace(" ", "")
            signal['current_ask'] =  lines[8].split(":")[1].replace(" ","")
            signal['target_1'] = lines[9].split(":")[1].split(" ")[1]
            signal['target_2'] = lines[10].split(":")[1].split(" ")[1]
            signal['target_3'] = lines[11].split(":")[1].split(" ")[1]
            signal['stoploss'] = lines[12].split(":")[1].split(" ")[1]
            signal['volume_symbol_a'] = lines[13].split(":")[1].replace(" ","")
            signal['volume_symbol_b'] = lines[14].split(":")[1].replace(" ","")
            signal['rsi'] = lines[15].split(":")[1].replace(" ","")
            return SignalMockup(signal)
        else:
            print("This was not a signal...")
    
    parsed_signal = parse(event.text)
    print(str(parsed_signal))
    

client.start()
client.run_until_disconnected()