from binance.client import Client
import subprocess
import time
from com_goldenthinker_trade_logger.Logger import Logger

class Utils:
    

    @classmethod
    def line_prepender(filename, line):
        with open(filename, 'r+') as f:
            content = f.read()
            f.seek(0, 0)
            f.write(line.rstrip('\r\n') + '\n' + content)
            
            
    @classmethod
    def precision(cls,symbol,float_value):
        client = Client('xoAWbPN2iKaPiGiQZ4TiFZ0yq2AvIdO4hBw8WrjA4AsFseXNbJ09Vd6wOAc8Siaw', 'Ex3dbvWjN5DgpEm960nd2M2pFz40JuqQiOVmB61X23VZEifFH0fYu6CDo7yZBvra')
        info = client.get_symbol_info(symbol=symbol)
        price_filter = float(info['filters'][0]['tickSize'])
        precision = info['quoteAssetPrecision']
        return ("{:." + str(precision) + "f}").format(float_value)
    
    
    @classmethod
    def normalice_quantity_for_lot_size(cls,symbol,float_value):
        client = Client('xoAWbPN2iKaPiGiQZ4TiFZ0yq2AvIdO4hBw8WrjA4AsFseXNbJ09Vd6wOAc8Siaw', 'Ex3dbvWjN5DgpEm960nd2M2pFz40JuqQiOVmB61X23VZEifFH0fYu6CDo7yZBvra')
        info = client.get_symbol_info(symbol=symbol)
        step = float(info['filters'][2]['stepSize'])
        qty = (int(float_value / step) + 1) * step
        precision = info['quoteAssetPrecision']
        return ("{:." + str(precision) + "f}").format(qty)
    
    
    @classmethod
    def group_dict_by(cls,my_dict,key_substr):
        new_dict = my_dict
        new_dict[key_substr] = []
        target_keys = [k for k in list(my_dict.keys()) if key_substr in k]
        for key in target_keys:
            if key!=key_substr:
                new_dict[key_substr].append(my_dict[key])
                new_dict.pop(key)
        return new_dict
            
    
    @classmethod        
    def percent_of(cls,x,of):
        return (x/100)*of
    
    
    @classmethod
    def execute(cls,command):
        try:
            batcmd=command
            time.sleep(5)
            o1 = str(subprocess.check_output(batcmd, shell=True,text=True))
            time.sleep(5)
            if o1 != None:
                return o1
            else:
                try:
                    o2 = str(subprocess.getoutput(batcmd)) 
                    #Logger.log("Executed command using getoutput as check_output smtimes fails :" + str(command))
                    time.sleep(5)
                    return o2
                except Exception(e):
                    Logger.log("Error executing command :" + str(command))
        except subprocess.CalledProcessError:
            o2 = str(subprocess.getoutput(batcmd))
            #Logger.log("Executed command using getoutput as check_output smtimes fails :" + str(command))
            time.sleep(5)
            return o2
            