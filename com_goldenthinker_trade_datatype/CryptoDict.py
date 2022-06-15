
from datetime import date, datetime,timedelta
from com_goldenthinker_trade_logger.Logger import Logger
import Levenshtein
import json

class CryptoDict:
    
    
    def __init__(self,my_dict,fields_to_avoid=[]):
        self.my_dict = my_dict
        self.fields_to_avoid = ['symbol','rise','drop','len','max_tick_value_timestampt','min_tick_value_timestampt','timestampt','type','_id'] + fields_to_avoid
        self.types_to_avoid = [date,datetime,str]
    
    def same_keys(self,d1):
        return set(self.my_dict.keys() - self.fields_to_avoid) == set(d1.keys() - self.fields_to_avoid)  

    # def more_or_less_same_keys(self,d1,tolerance=2):
    #     ks = list(set(self.my_dict.keys() - self.fields_to_avoid))
    #     ks1 = list(set(d1.keys() - self.fields_to_avoid))
 
    #     result = len([ (k,k1) for k in ks for k1 in ks1 if Levenshtein.distance(k,k1) <= tolerance ]) > 0
        
    #     return set(self.my_dict.keys() - self.fields_to_avoid) == set(d1.keys() - self.fields_to_avoid)

    def keys(self):
        return self.my_dict.keys()
    
    def fuzzy_get(self,key):
        min_distance = 9999
        min_distance_key = ''
        for k in self.my_dict.keys():
            distance = Levenshtein.distance(k,key)
            if distance<=min_distance:
                min_distance = distance
                min_distance_key = k
        return self.my_dict.get(min_distance_key)
    
    
    def add_numbers_binary_operator(self,a,b):
        if type(a) not in self.types_to_avoid and type(b) not in self.types_to_avoid:
            return a + b

    
    def sub_numbers_binary_operator(self,a,b):
        if type(a) not in self.types_to_avoid and type(b) not in self.types_to_avoid:
            return a - b
    
    def mul_numbers_binary_operator(self,a,b):
        if type(a) not in self.types_to_avoid and type(b) not in self.types_to_avoid:
            return a * b

    
    def div_numbers_binary_operator(self,a,b):
        if type(a) not in self.types_to_avoid and type(b) not in self.types_to_avoid:
            return a / b

    
    
    def __truediv__(self,d1):
        return self.operations_template(d1,self.div_numbers_binary_operator)
         
    def __add__(self,d1):
        return self.operations_template(d1,self.add_numbers_binary_operator)
            
    
    def __sub__(self,d1):
        return self.operations_template(d1,self.sub_numbers_binary_operator)

    def __mul__(self,d1):
        return self.operations_template(d1,self.mul_numbers_binary_operator)

    def __str__(self):
        res = "{"
        for k in self.my_dict.keys():
            curr_val = self.my_dict.get(k)
            if (type(curr_val)==CryptoDict):
                res = res + str(k) + " : " +  str(curr_val)
            else:
                res = res + str(k) + " : " +  str(curr_val)
            res = res + ','
        res = res + "}"
        return res
       


    def any_value_of_type(self,t):
        ks = [ self.my_dict.get(k) for k in self.my_dict.keys() ]
        ks1 = []
        for each_value_type in ks:
            ks1.append(type(each_value_type))
        return t in ks1


    
    
    def operations_template(self,d1,binary_operation):
        if type(d1) is int or type(d1) is float:
            res_sum = {key: binary_operation(self.fuzzy_get(key),d1) for key in set(self.my_dict.keys()) if key not in self.fields_to_avoid and (type(self.fuzzy_get(key) is int) or type(self.fuzzy_get(key) is float))}
            return res_sum
        else:
            #if self.same_keys(d1):
            if (type(d1) is CryptoDict):
                res_sum = dict()
                if not self.any_value_of_type(dict):
                    res_sum = {key: binary_operation(self.fuzzy_get(key),d1.fuzzy_get(key)) for key in set(self.my_dict) | set(d1.my_dict) if key not in self.fields_to_avoid }
                else:
                    res_sum =  ({key: binary_operation(self.fuzzy_get(key),d1.fuzzy_get(key))
                                for key in set(self.my_dict) | set(d1.my_dict) 
                                if (key not in self.fields_to_avoid) 
                                if (type(self.fuzzy_get(key)) is not dict and type(d1.fuzzy_get(key)) is not dict)} |
                                {key: binary_operation(CryptoDict(self.fuzzy_get(key)),CryptoDict(d1.fuzzy_get(key))) 
                                for key in set(self.my_dict.keys()) 
                                if (type(self.fuzzy_get(key)) is dict and type(d1.fuzzy_get(key)) is dict)})
            else:
                if type(d1) is dict:
                    res_sum = self + CryptoDict(d1)
                else:
                    return 0
            if type(res_sum) is not CryptoDict:
                return CryptoDict(res_sum)
            else:
                return res_sum
    
    
    
    def dict_copy_keep_same_keys(self,d2):
        return CryptoDict({k2:v2 for (k2,v2) in d2.get_plain_dict().items()})
    
    def dict_merge(self,d1,d2):
        difference = {k1:v1 for (k1,v1) in d1.get_plain_dict().items() if d2.fuzzy_get(k1)==None}
        self.my_dict = d2 | difference
        return CryptoDict((d2 | difference))
    
    def check_if_sequence_within_requested_time(self,amount_of_minutes):
        if self.fuzzy_get('timestampt') != None:
            return ((self.fuzzy_get('timestampt') >= (datetime.now() - timedelta(minutes=amount_of_minutes))) and
                (self.fuzzy_get('timestampt') < datetime.now()))
        else:
            Logger.log("Error comparing if sequence is within a range of minutest")
            return False
        
    def add_map(self,k,v):
        self.my_dict[k] = v
        
    def get_map(self,k):
        return self.my_dict.get(k)
        
    def get_type(self):
        return self.my_dict.get('type')
    
    def get_plain_dict(self):
        return self.my_dict
    
    def set_dict(self,d):
        self.my_dict = d
        
    