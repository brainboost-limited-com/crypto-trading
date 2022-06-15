from com_goldenthinker_trade_telegram.TelegramNotifier import TelegramNotifier
from com_goldenthinker_trade_datasource_network.SocketReceive import SocketReceive
import datetime



class ProcessMonitor:
    
    time_stampt_table = dict()
    
    
    def __init__(self,processes_names,expected_frequency):
        self.process_to_monitor = processes_names      
        self.telegram = TelegramNotifier.get_instance()
        self.frequency = expected_frequency
        self.last_message_timestampt = datetime.datetime.now()
        
        for p in processes_names:
            ProcessMonitor.time_stampt_table[p] = datetime.datetime.now()
        



    def start(self):
        socket_receive = SocketReceive()
        socket_receive.listen(self.receive)


    def receive(self,message):
        report_i_am_alive = message
        ProcessMonitor.time_stampt_table[report_i_am_alive] = datetime.datetime.now()
        while (datetime.datetime.now() - ProcessMonitor.time_stampt_table[report_i_am_alive]) <= datetime.timedelta(minutes=self.frequency):
            print("waiting new notification.. else will trigger telegram alert..")
        self.telegram.send_message(message="ALERT: Process " + report_i_am_alive + " is not sending updates.")




pm = ProcessMonitor(['monitor_all_symbols.py','monitor_individual_symbols.py'],3)
pm.start()



    
    
