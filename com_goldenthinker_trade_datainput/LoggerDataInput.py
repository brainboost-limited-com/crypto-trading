from com_goldenthinker_trade_datainput.DataInput import DataInput
from com_goldenthinker_trade_logger.Logger import Logger

class LoggerDataInput(DataInput):
    
    def __init__(self):
        super().__init__(system=Logger, name='logger')
        
        
    def input(data='',*args):
        try: 
            Logger.log(args[0],telegram=args[1].get('telegram'))
        except:
            return False
        return True