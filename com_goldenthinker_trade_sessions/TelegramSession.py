from datetime import datetime
from telethon import TelegramClient, events


class TelegramSession:
    
    
    def __init__(self):
        api_id = 3820623
        api_hash = 'de74cd9776235755c03d27cc0d4b1507'
                
        telethon_session_name = 'robot'
        session_str = 'telethon_'+telethon_session_name+'_session'
        self.client = TelegramClient(session_str, api_id, api_hash)
    
    
    def get_client(self):
        self.client.start()
        return self.client
            
            
            