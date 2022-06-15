#----------------------- How to execute supervisor process --------------------

# command_running_forever
#^Z
#zsh: suspended  command_running_forever
#bg
#[1]  + continued  command_running_forever
#jobs
#[1]  + running    command_running_forever
#disown %1
#logout

import subprocess

from com_goldenthinker_trade_logger.Logger import Logger
import time


def execute(command):
	try:
		batcmd=command
		return str(subprocess.check_output(batcmd, shell=True,text=True))
	except:
		Logger.log("error executing commmand :" + str(command))


def ticker_is_running(output):
	return ('python monitor_all_symbols.py' in output)


def morning():
	Logger.log("Executing morning scripts:  crawler.py ",telegram=True)
	execute('python crawler.py')

def middle_day():
	Logger.log('Middle Day tasks.',telegram=True)

def afternoon():
	Logger.log('Afternoon tasks.',telegram=True)

def night():
	Logger.log('Night tasks.',telegram=True)
 
def evening():
    Logger.log('Evening tasks.',telegram=True)



def day_triggers(execu=True):
	if execu is True:
		currentTime = int(time.strftime('%H'))
		
		if currentTime < 12 :
			morning()
		if currentTime > 12 :
			afternoon()
		if currentTime==12:
			middle_day()
		if currentTime > 6 :
			evening()

def start_telegram_gateway():
	print('python telegram_webgateway.py &')
	execute('python telegram_webgateway.py &')

def telegram_is_running(output):
	return ('python telegram_webgateway.py' in output)


while True:
	#start_telegram_gateway()
	#day_triggers()
	p = Utils.execute('ps aux')
	if telegram_is_running(p):
		print("telegram is running")
	if not telegram_is_running(p):
		start_telegram_gateway()
		time.sleep(30)
		Logger.log('python telegram_webgateway.py not running, restored...',telegram=True)
	else:
		if not ticker_is_running(p):
			Utils.execute('python monitor_all_symbols.py &')
			Logger.log('python monitor_all_symbols.py was not running, restored...',telegram=True)

	
