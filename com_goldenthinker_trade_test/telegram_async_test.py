import sys

if 'com_goldenthinker_trade_model.SignalParserNew' not in sys.modules:
    from com_goldenthinker_trade_model_parsers.SignalParserNew import SignalParserNew

from com_goldenthinker_trade_model_order.Order import Order
from telethon.tl import functions

from datetime import datetime
from telethon import client,events
from telethon import TelegramClient
import asyncio
from binance.exceptions import BinanceAPIException
        
api_id = 3820623
api_hash = 'de74cd9776235755c03d27cc0d4b1507'


telethon_session_name = 'robot'
session_str = 'telethon_'+telethon_session_name+'_session'
        
print("SESSION: "+session_str)
client = TelegramClient(session_str, api_id, api_hash)



event_markup = dict()
datetimeObject = datetime.now()
        



async def channels_to_listen():
    search = ['signal','free signale','crypto','crypto signal','binance','bitcoin']
    channels_to_listen = []
    for each_term in search:
        channels = await client(functions.contacts.SearchRequest(q=each_term,limit=1000))
        for each_channel in channels.chats:
            if each_channel.username!=None:
                channels_to_listen.append('@'+each_channel.username)

@client.on(events.NewMessage(incoming=True))
async def my_event_handler(event):
    chat_from = event.chat if event.chat else (await event.get_chat())
    try:
        signal_from_text = SignalParserNew(timestampt=str(event.date),unstructred_text=event.text,channel=('@' + chat_from.username)).parse()
        if signal_from_text!=None:
            if signal_from_text.valid():
                signal_from_text.save()
                print(signal_from_text.signal) #return message.textx
                print("Analysing previous similar signals... " + str(signal_from_text))
                order = Order(signal_from_text)
                order.execute()
    except BinanceAPIException as e:
        print(str(e))
        if ("-1013): Filter failure: PRICE_FILTER" in str(e)):
            print("The asset price is higher")
    except TypeError as e:
        print("Signal not valid ")

        
        

client.start()
client.run_until_disconnected()

    

loop = asyncio.get_event_loop()
loop.run_until_complete(channels_to_listen())
