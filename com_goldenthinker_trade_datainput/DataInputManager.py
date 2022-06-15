from com_goldenthinker_trade_datainput.LoggerDataInput import LoggerDataInput
from com_goldenthinker_trade_datainput.DataInput import DataInput


class DataInputManager:
    
    _data_input = dict()
    
    logger = LoggerDataInput()
    _data_input[logger.get_name()] = logger
    
      
    
    @classmethod
    def get_input(cls,name):
        return cls._data_input.get(name)