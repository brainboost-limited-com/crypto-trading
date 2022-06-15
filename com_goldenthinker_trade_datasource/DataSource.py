from datetime import datetime



class DataSource:
    
    
    # A data source may consume other data sources to produce its data
    def __init__(self,name:str='',trust:float=0.99999999,session=None,consumers=[]):
        self.trust = trust
        self.name = name
        self.session = session
        self.consumers = consumers
        self.id = hash(str(datetime.now()) + str(name) + str(self.trust))
    
    
    
    def start(self):
        for ds in self.consumers:
            ds.subscribe(self)
            ds.start()
    
    
       
    def update(self,data):
       for c in self.consumers:
           c.notify(data)
   
   
    def subscribe(self,consumer):
        self.consumers.append(consumer)
    
    
    def get_name(self):
        return self.name
    