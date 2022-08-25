from telethon import TelegramClient, events
from com_goldenthinker_trade_database.MongoConnector import MongoConnector
from com_goldenthinker_trade_model_parsers.SignalParser2 import SignalParser2

from com_goldenthinker_trade_logger.Logger import Logger

api_id = 3820623
api_hash = 'de74cd9776235755c03d27cc0d4b1507'

client = TelegramClient('telethon_robot_session.session', api_id, api_hash)

Logger.set_process_name(name='gt_telegram_incoming_signal')


@client.on(events.NewMessage)
async def my_event_handler(event):
    chat_from = event.chat
    if chat_from != None and type(chat_from.username)==str:
        #Logger.log('Received message from channel @' + chat_from.username)
        channel_name = '@' + chat_from.username
        channel = client.get_entity(channel_name)
        message = event.message.raw_text
        if (message!=None):
            try:   # fix: process signal if not already in database , i can check by timestampt
                signal_parser = SignalParser2(timestampt=str(event.message.date),unstructred_text=message,channel=channel_name)
                s = signal_parser.parse()
                if s!=None:
                    if s.valid():
                        s.save()
                        MongoConnector.get_instance().save_signal(s.signal)
                        Logger.log('Signal inserted: ' + str(s.signal),external=True) #return message.text
            except TypeError:
                Logger.log("Signal not valid",external=True)
        Logger.log('{}'.format(event),external=True)

client.start()
client.run_until_disconnected()