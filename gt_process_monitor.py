#----------------------- How to execute supervisor process --------------------
# Makes sure all processes are running, records shortage gaps and re executes processes if
# they die for any reason. Sends telegram notifications on all events and on emergency

# Despite processes are alive it also makes sure that no process ends up idle , by checking 
# the centralised logs with each process tag name per line, and if there was no input from a process lets say
# in the last 5 min ,  it kills and restarts the process implemented as a linux service.

#  Linux services are stored in the server itself at /etc/systemd/system/*.service
#  The linux services coded in this project are in ec2/etc/systemd/system, you will 
#  have to copy these services to the server directory 

# To make any process not die despite the terminal session is terminated do as follows:

#
# command_running_forever
# ^Z
# zsh: suspended  command_running_forever
# bg
# [1]  + continued  command_running_forever
# jobs
# [1]  + running    command_running_forever
# disown %1
# logout

import subprocess
import os
from com_goldenthinker_trade_logger.Logger import Logger
import datetime
import time
from com_goldenthinker_trade_utils.Utils import Utils






def is_process_alive(process_name):
	out_command = Utils.execute('ps aux | grep python| grep -v grep') + str(Utils.execute('ps aux | grep mongod| grep -v grep')) + str(Utils.execute('ps aux | grep gt_web_ui_dashboard grep -v grep'))
	return process_name in out_command


def process_had_updated_in_the_last_minutes(process_name,mins=5):

	last_time = datetime.datetime.now()
	log_file_date = last_time.strftime("%Y_%m_%d")
	log_file = "logs/trader_log-" + log_file_date + ".csv"
	with open(log_file, 'r') as f:

		i = -1
		last_time_updated = 0
		Logger.log("Checking updates for : " + process_name)
		lines = f.readlines()


		if i > len(lines)*-1:
			last_line = lines[i]
			process_from_line = last_line.split(',')[0]
			if process_from_line==process_name:
				i = 1
				last_time_updated = datetime.datetime.strptime(last_line.split(',')[1], '%Y-%m-%d %H:%M:%S.%f')
				Logger.log('checking '+str(last_time_updated))
				p_alive = is_process_alive(process_name)
				Logger.log('checking '+str(last_time_updated))
				last_time_updated_within_last_5_min = ((datetime.datetime.now() - last_time_updated) <= datetime.timedelta(minutes=mins))
				Logger.log(str(p_alive and last_time_updated_within_last_5_min))
				return p_alive and last_time_updated_within_last_5_min
			else:
				i = i - 1
	return False



Logger.set_process_name('gt_process_monitor')

# services need to be started in order, the service process monitor (this service)
# should start the other ones

# The telegramweb gateway is the service that sends all notifications by telegram to
# the subscribers (or traders)
if not is_process_alive('mongod'):
	Utils.execute('service mongod start')

processes = ['gt_monitor_all_symbols','gt_sell','gt_buy','gt_performance_backtesting','gt_signals_from_telegram_crawler','gt_telegram_webgateway','gt_web_ui_dashboard']

# Because some processes do not output to logs frequently do not take them a crashed
# but manage them anyway 
do_not_check_log_output = ['gt_web_ui_dashboard','mongod']


for each_process in processes:
    if not is_process_alive(each_process):
        Logger.log(str(each_process) +" service is dead...",telegram=True)
        Utils.execute('systemctl start ' + str(each_process))
        Logger.log(str(each_process) +" service is starting...",telegram=True)



Logger.log("process_monitor service is starting...",telegram=True)

#if not os.geteuid() == 0:
#	Logger.log("Only root can run this script")
#	print('Only root can execute this script')
#else:
while True:
	for each_process in processes:
		# Before working with each process we check if is not later than 12:00 am so we chmod 777 the logs
		# as setting default access permissions for the new log file in never works, so here we have more control, 
		# also crond has a strange syntax, it is difficult to test and it does not even work by generating the config file
		# using a GUI, here in python we have more control
		if_later_than_12am_set_new_default_access_permission_for_new_log_file()
		# Continue checking processes status
		if not each_process in do_not_check_log_output:
			Logger.log('checking '+str(each_process))
			p = process_had_updated_in_the_last_minutes(each_process)
			if not p:
				Logger.log(str(each_process) + ' is not running, restoring...',telegram=True)
				o1 = Utils.execute('service ' +  each_process +  ' stop')    # kill process in case is alive doing nothing
				Logger.log(str(o1))
				o3 = Utils.execute('service ' +  each_process +  ' start')
				Logger.log(str(o3))
			else:
				Logger.log(str(each_process) + 'is running properly, wait 60 seconds before recheck...')
			time.sleep(60)
			if 'Active: active (running)' not in execute('service mongod status'):
				Logger.log('MongoDB not running... restarting MongoDB')
				Utils.execute('service mongod start')
