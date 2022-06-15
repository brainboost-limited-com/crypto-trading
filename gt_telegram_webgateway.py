from com_goldenthinker_trade_logger.Logger import Logger
from com_goldenthinker_trade_telegram.TelegramNotifier import TelegramNotifier
import cherrypy
import datetime

class TelegramWebGateway(object):
    
    _telegram_notifier = TelegramNotifier.get_instance()

    process_alive_signal = dict()
    processes = ['gt_monitor_all_symbols','gt_robot','gt_process_monitor']
    
    @cherrypy.expose
    def send_telegram_notification(self,message,public='False'):
        TelegramWebGateway.process_alive_signal[message.split(',')[0]] = datetime.datetime.now()
        if public=='True':
            public = True
        TelegramWebGateway._telegram_notifier.send_message(message=message,public=public)
        for k in TelegramWebGateway.process_alive_signal.keys():
            # If there was no log input for the process in 5 min
            if ((datetime.datetime.now() - TelegramWebGateway.process_alive_signal[k]) > (datetime.timedelta(minutes=5))):
                if str(k) in TelegramWebGateway.processes:
                    TelegramWebGateway._telegram_notifier.send_message(message=str(k)+" process is not running")
                    
                    
                    
    @cherrypy.expose
    def send_message_to_user(self,message,username):
        TelegramWebGateway._telegram_notifier.send_message(message=message,username=username)
    
    
    
    
Logger.set_process_name(name='gt_telegram_webgateway')
Logger.log("Start Telegram Gateway")
TelegramWebGateway._telegram_notifier.send_message(message="Telegram WebGateway starting...")
cherrypy.config.update({'server.socket_host': '0.0.0.0'})
cherrypy.quickstart(TelegramWebGateway())