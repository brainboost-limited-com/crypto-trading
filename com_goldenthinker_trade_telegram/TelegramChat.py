
from telethon.tl import functions

from datetime import datetime
from telethon import client,events
from telethon import TelegramClient
import re
import asyncio

        
api_id = 3820623
api_hash = 'de74cd9776235755c03d27cc0d4b1507'

datetimeObject = datetime.now()
session_str = 'com_goldenthinker_trade_sessions_data/'+ "session_telegram_" +  datetimeObject.strftime('%Y%m%d%H%M%S')
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
    try:
        signal_from_text = Signal(str(event.date),event.text,'@' + event.chat.username)
        if signal_from_text.valid():
            signal_from_text.signal.save()
            print(signal_from_text.signal) #return message.text
            print("Analysing previous similar signals... " + signal_from_text)
            order = Order(signal_from_text)
            order.execute()
    except TypeError:
        print("Signal not valid")
        

client.start()
client.run_until_disconnected()

    

loop = asyncio.get_event_loop()
loop.run_until_complete(channels_to_listen())
