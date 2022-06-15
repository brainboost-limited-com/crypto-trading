
import subprocess
import os
from com_goldenthinker_trade_logger.Logger import Logger
import datetime
import time

def execute(command):
	try:
		batcmd=command
		return str(subprocess.check_output(batcmd, shell=True,text=True))
	except:
		Logger.log("Error executing commmand :" + str(command),telegram=True)

Logger.set_process_name('gt_compress_logs')


Logger.log('Compressing logs for today find them in storage/logs',telegram=True)


files = Utils.execute('ls logs/').split('\n')
for f in files: 
    Logger.log('Compressing log to zip file' + str(f) )
    o = Utils.execute('7z a -m0=lzma2 -mx storage/logs/' + str(f).split('.')[0] + '.7z' + ' logs/'+str(f))
    Logger.log('Compressor output: ' + str(o))
    o1 = Utils.execute('rm logs/' + str(f))
    Logger.log('Original file ' + str(f) + ' is deleted, to get it back execute:   7z x storage/logs/file.7z ')

Logger.log('Today s logs have been compressed and stored ')


