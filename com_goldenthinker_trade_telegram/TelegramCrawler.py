import asyncio
from com_goldenthinker_trade_model_parsers.SignalParser2 import SignalParser2
from com_goldenthinker_trade_database.TinyDbConnector import TinyDbConnector
import re
import time
from telethon.errors.rpc_error_list import ChannelInvalidError, ChannelPrivateError, ChannelsTooMuchError, FloodWaitError
from tinydb.database import TinyDB
from tinydb import where
from com_goldenthinker_trade_sessions.TelegramSession import TelegramSession
from com_goldenthinker_trade_model_signals.Signal import Signal
from telethon.tl import functions
from telethon.tl.functions.channels import JoinChannelRequest
from telethon.errors.rpc_error_list import FloodWaitError
import random
from com_goldenthinker_trade_model_parsers.SignalParser2 import SignalParser2
from com_goldenthinker_trade_database.MongoConnector import MongoConnector

class TelegramCrawler:
    
    def __init__(self,update_channels=False):
        self.client = TelegramSession().get_client()
        self.update_channels = update_channels
        
    def crawl_for_signals(self):
        
        def main():
            if self.update_channels:
                channels = TinyDbConnector.get_channels()
                for c in channels:
                    try:
                        time.sleep(random.randint(1, 20))
                        a = self.client(JoinChannelRequest(c['channel']))
                        print("Request sent for: " + c['channel'] + " result: " + str(a))
                        TinyDbConnector.remove_channel(c['channel'])
                    except ChannelsTooMuchError:
                        print(c['channel'] + " tried many times")
                    except ChannelInvalidError:
                        print(c['channel'] + " invalid")
                        TinyDbConnector.remove_channel(c['channel'])
                    except ChannelPrivateError:
                        print(c['channel'] + " is private")
                        TinyDbConnector.remove_channel(c['channel'])
                    except TypeError:
                        print(c['channel'] + " is not a channel but a normal user.")
                        TinyDbConnector.remove_channel(c['channel'])
                    except ValueError:
                        print(c['channel'] + " does not exist.")
                        TinyDbConnector.remove_channel(c['channel'])
                    except Exception as e:
                        print(c['channel'] + " has another error.")
                        print(str(e))
                        TinyDbConnector.remove_channel(c['channel'])
                        seconds = re.findall(r"\d+",str(e))
                        if len(seconds)==1:
                            print("Waiting " + str(seconds[0]) + " seconds...")
                            time.sleep(int(seconds[0]) + 1)
                    
                #except ResolveUsernameRequest:
                #    print("Wait 348 sec...")
                #    time.sleep(348)
            
            # Searches for messages in all the chat rooms that contain the following words        
            search = ['signal','free signal','buy','target','stoploss','crypto','crypto signal','binance','bitcoin']
            
            processed_channels = TinyDbConnector.instance_for_channels().channels_processed_so_far()
            
            for each_term in search:
                print("Searching term: " + each_term)
                channels_all = self.client(functions.contacts.SearchRequest(q=each_term,limit=1000))
                channels = [x for x in channels_all.chats if x.username not in processed_channels]
                for each_channel in channels:
                    try:
                        if each_channel.username!=None:
                            print('@' + each_channel.username)
                            channel_name = '@' + each_channel.username
                            channel = self.client.get_entity(channel_name)
                            messages = self.client.get_messages(channel, limit= 5000) #pass your own args
                            #then if you want to get all the messages text
                            for x in messages:
                                if (x.text!=None):
                                    try:   # fix: process signal if not already in database , i can check by timestampt
                                        signal_parser = SignalParser2(timestampt=str(x.date),unstructred_text=x.text,channel=each_channel.username)
                                        s = signal_parser.parse()
                                        if s!=None:
                                            if s.valid():
                                                s.save()
                                                print(s.signal) #return message.text
                                                MongoConnector.get_instance().save_signal(s.signal)
                                    except TypeError:
                                        print("Signal not valid")
                    except FloodWaitError as e:
                        seconds = re.findall(r"\d+",str(e))
                        if len(seconds)==1:
                            print("Waiting " + str(seconds[0]) + " seconds...")
                            time.sleep(int(seconds[0]) + 1)
                            


        loop = asyncio.get_event_loop()
        loop.run_until_complete(main())
        print("Signals ready in json file")
        return True
