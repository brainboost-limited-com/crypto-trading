import asyncio
import re
from abc import abstractmethod
from dataclasses import replace
from datetime import datetime
from os.path import split
import time

import dateutil
from dateutil.parser import ParserError, parse
from pygments.lexer import include
from telethon import TelegramClient, events
from telethon.errors.rpcerrorlist import FloodWaitError
from telethon.tl import functions, types
from tinydb import Query, TinyDB
from com_goldenthinker_trade_model.Signal import Signal


api_id = 3820623
api_hash = 'de74cd9776235755c03d27cc0d4b1507'
db = TinyDB('com_goldenthinker_trade_model/signals.json')


datetimeObject = datetime.now()
session_str = "session_telegram_" + datetimeObject.strftime('%Y%m%d%H%M%S')
print("SESSION: "+session_str)
client = TelegramClient(session_str, api_id, api_hash)

client.start()


    
#channels = ['@AnnyDeCrypto_bot','@QualitySignalsChannel',]

async def main():
    try:
        search = ['signal','free signale','crypto','crypto signal','binance','bitcoin']
        for each_term in search:
            print("Searching term: " + each_term)
            channels = await client(functions.contacts.SearchRequest(q=each_term,limit=1000))
            for each_channel in channels.chats:
                if each_channel.username!=None:
                    print('@' + each_channel.username)
                    channel_name = '@' + each_channel.username
                    channel = await client.get_entity(channel_name)
                    messages = await client.get_messages(channel, limit= 20000) #pass your own args
                    #then if you want to get all the messages text
                    for x in messages:
                        if (x.text!=None):
                            try:
                                s = Signal(when_signal_occurred=str(x.date),signal_unstructured_text=x.text,channel_name=each_channel.username)
                                if s.valid():
                                    s.save()
                                    print(s) #return message.text
                                else:
                                    s = Signal(when_signal_occurred=str(x.date),signal_text_for_smarter_parser=x.text,channel_name=each_channel.username)
                                    s.save()
                            except TypeError:
                                print("Signal not valid")
    except FloodWaitError as e:
        seconds = re.findall(r"\d+",str(e))
        if len(seconds)==1:
            print("Waiting " + str(seconds[0]) + " seconds...")
            time.sleep(int(seconds[0]) + 1)


loop = asyncio.get_event_loop()
loop.run_until_complete(main())