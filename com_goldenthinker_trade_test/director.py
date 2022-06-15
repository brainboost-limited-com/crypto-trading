from com_goldenthinker_trade_telegram.TelegramNotifier import TelegramNotifier
import subprocess

import time

subprocess = subprocess.Popen("ps aux|grep monitor_all_symbols.py", shell=True, stdout=subprocess.PIPE)
subprocess_return = subprocess.stdout.read()

print(subprocess_return)

if str(subprocess_return).count("monitor_all_symbols.py")==2:
    print("ticker is running...")



while True:
    pass

