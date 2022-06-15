# ret = dict()
# ret['value'] = 4
# ret['timestampt'] = 243344453
# ret['value_delta'] = 234
# ret['time_delta'] = 43434
# print(str(ret))

# retq = dict()
# retq['value'] = 4
# retq['timestampt'] = 243344453
# retq['value_delta'] = 234
# retq['time_delta'] = 43434
# print(str(retq))

# a = []
# a.append(ret)
# a.append(retq)
from com_goldenthinker_trade_monitor.Tick import Tick


a = Tick(232453)

print(str(a))