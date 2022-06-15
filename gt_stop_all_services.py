import subprocess
from com_goldenthinker_trade_logger.Logger import Logger
import time
from com_goldenthinker_trade_utils.Utils import Utils


Logger.set_process_name('gt_stop_all_services')


processes = ['gt_process_monitor','gt_monitor_all_symbols','gt_sell','gt_buy','gt_signals_from_telegram_crawler','gt_telegram_webgateway','gt_web_ui_dashboard','mongod']



for p in processes:
    p_status = Utils.execute('service ' + p + ' status')
    if 'Active: active (running)' in p_status:
        Utils.execute('service ' + p + ' stop')
        Logger.log("Service " + p + " stopped")
    