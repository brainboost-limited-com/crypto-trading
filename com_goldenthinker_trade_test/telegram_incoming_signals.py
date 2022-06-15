from datetime import datetime
from com_goldenthinker_trade_logger.Logger import Logger
from telethon import TelegramClient,events



api_id = 3820623
api_hash = 'de74cd9776235755c03d27cc0d4b1507'
client = TelegramClient('session_telegram_20211115004745.session',api_id,api_hash)
client.updates.workers = 1
client.start()

    
@client.on(events.NewMessage(outgoing=False)) # all incoming messages
def my_event_handler(event): 
    sender = event.get_sender()
    newMessage = event.message.message # this is only a telegram message content, its what u see on telegram 
    FullMessage = event.message # this is full message event, with technical things undergoingm like some True, False, etc, and with buttons if any.
    time = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
    print(newMessage)
    print(FullMessage)


client.start()
try:
    print('(Press Ctrl+C to stop this)')
    client.loop.run_until_disconnected()
finally:
    client.disconnect()