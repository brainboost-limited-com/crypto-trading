import datetime
from dateutil.parser import parse
import json

class Date:
    
    
    
    def __init__(self,date_str=None,date_int=None,date_obj=None):
        if date_str!=None:
            self.parsed_date = parse(date_str)
        if date_int!=None:
            self.parsed_date = self.integerdate(date_int)
        if date_obj!=None:
            self.parsed_date = date_obj
            
    def now(self):
        return datetime.datetime.now()
    
    def now_yyyymmdd_str(self):
        return self.now().strftime("%Y_%m_%d")
    
    def integerdate(self,date_str_int):
        return (datetime.datetime.fromtimestamp(int(date_str_int)/1000)).replace(tzinfo=None)
    
    def kline_date(self,date_str_int):
        return self.integerdate(date_str_int)
    
    
    def add_days(self, amount_of_days=0):
        return Date(date_obj=((self.parsed_date + datetime.timedelta(days=amount_of_days)).replace(tzinfo=None)))
    
    def __sub__(self, another_date):
        return (self.parsed_date - another_date)
    
    def formatted_date(self):
        return str(self.parsed_date.strftime("%d %b, %Y"))
    
    def serialize(self,d):
        return str(d)
    
    def time_difference_in_min(self,t1,t2):
        if t1 > t2:
            td = t1 - t2
        else:
            td = t2 - t1
        return int(round(td.total_seconds() / 60))
    
    
    def int_current_timestampt(self):
        return int(datetime.datetime.now().strftime("%Y%m%d%H%M%S%f"))
    
    def timestampt_mongo(self):
        return datetime.datetime.utcnow()