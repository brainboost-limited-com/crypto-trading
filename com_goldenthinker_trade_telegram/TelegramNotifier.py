from telethon import TelegramClient
from com_goldenthinker_trade_logger.Logger import Logger
from telegram import ParseMode
import psutil
import os


class TelegramNotifier:
    
    _instance = None
    phone = "3538346520983"
    public_users = []
    
    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = cls.__new__(cls)
            cls._instance.api_id = 3820623
            cls._instance.api_hash = 'de74cd9776235755c03d27cc0d4b1507'
            #cls._instance.session_str = "session_telegram_" + datetime.datetime.now().strftime('%Y%m%d%H%M%S')

            # Obtain list of users subscribed to the signals
            with open("users.list", 'r') as f:
                symbols_to_monitor = f.read().split('\n')
                for s in symbols_to_monitor:
                    cls.public_users.append(s)

            
            telethon_session_name = 'robot'
            cls._instance.session_str = 'com_goldenthinker_trade_sessions_data/' + 'telethon_'+telethon_session_name+'_session'
            print("SESSION: "+cls._instance.session_str)
            cls._instance.client = TelegramClient(cls._instance.session_str, cls._instance.api_id, cls._instance.api_hash)
            cls._instance.client.start()
        return cls._instance
        
        
    def send_message(self,username='golden_thinker_pablo',message=None,public=False):
        if message is not None:
            receiver = self.client.get_input_entity(username)
            self.client.send_message(receiver, message.format(username),parse_mode=ParseMode.HTML)
        else:
            print("Message missing.")
        Logger.log("active_users: "+str(TelegramNotifier.public_users))
        if public == True:
            for u in TelegramNotifier.public_users:
                #Logger.log("active_users: "+str(TelegramNotifier.public_users),telegram=True)
                receiver = self.client.get_input_entity(u)
                self.client.send_message(receiver, message.format(u),parse_mode=ParseMode.HTML)
                #Logger.log("active_users: "+str(TelegramNotifier.public_users))
    
    
    def send_message_to_user(self,username='golden_thinker_pablo',message=None,message_to=None):
        if message is not None:
            receiver = self.client.get_input_entity(username)
            self.client.send_message(receiver, message.format(message_to),parse_mode=ParseMode.HTML)
        else:
            Logger.log('Message is none')
        
    
    