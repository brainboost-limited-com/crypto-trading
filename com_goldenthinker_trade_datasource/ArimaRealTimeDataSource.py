from decimal import Decimal
from com_goldenthinker_trade_datasource.RealTimeDataSource import RealTimeDataSource



class ArimaRealTimeDataSource(RealTimeDataSource):
    
    
    def __init__(self, name='', trust=Decimal(0.999999), session=None, consumers=...):
        super().__init__(name=name, trust=trust, session=session, consumers=consumers)
        
        
        
    def notify(self,data):
        pass    
    
        
    def start(self):
        pass
    