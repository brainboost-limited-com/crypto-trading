
from abc import abstractmethod
from datetime import datetime

class DataInput:
    
    def __init__(self,system=None,name=None):
        self.system = system
        self.name = name
        self.id = hash(str(datetime.now()) + str(name))
    
    @abstractmethod
    def input(data,*args):
        pass
    
    def get_name(self):
        return self.name
    
    def get_id(self):
        return self.id
    
    def get_system(self):
        return self.system