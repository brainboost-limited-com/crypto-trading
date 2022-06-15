import subprocess
from com_goldenthinker_trade_logger.Logger import Logger
import time
from com_goldenthinker_trade_utils.Utils import Utils

Logger.set_process_name('gt_start_all_services')


    
processes = ['mongod','gt_process_monitor']



for p in processes:
    p_status = Utils.execute('service ' + str(p) + ' status')
    if p_status != None:
        if not 'Active: active (running)' in p_status:
            Utils.execute('service ' + p + ' start')
            Logger.log("Service " + p + " started.")
        else:
            Logger.log("Cannot check if service has " + p + " started.")