from com_goldenthinker_trade_monitor.Tick import Tick

class MultipleTick:
    
    def __init__(self,ticks=[]):
        self.ticks = [Tick(x) for x in ticks]
        
        
    def get_ticks(self):
        return self.ticks