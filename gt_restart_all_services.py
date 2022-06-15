
import subprocess
import os
from com_goldenthinker_trade_logger.Logger import Logger
import time
from com_goldenthinker_trade_utils.Utils import Utils


Logger.set_process_name('gt_restart_all_services')




Utils.execute('service gt_process_monitor stop')

processes = ['gt_monitor_all_symbols','gt_sell','gt_buy','gt_performance_backtesting','gt_signals_from_telegram_crawler','gt_signal_performance','gt_telegram_webgateway','gt_web_ui_dashboard','mongod']

Logger.log("Restarting all services...")

for p in processes:
    Utils.execute('service ' + p + ' stop')
    
for p in processes:
    Utils.execute('service ' + p + ' start')
    
for p in processes:
    p_status = Utils.execute('service ' + p + ' status')
    if not 'Active: active (running)' in p_status:
        Logger.log("Failed to restart the service " + str(p),telegram=True,trace=True)
        

Utils.execute('service gt_process_monitor start')