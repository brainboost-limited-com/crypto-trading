from com_goldenthinker_trade_datasource.DataSource import DataSource

class OnDemandDataSource(DataSource):
    
    def __init__(self, name, trust=None, session=None) -> None:
        super().__init__(name, trust=trust, session=session)
        
    def update(self):
        pass