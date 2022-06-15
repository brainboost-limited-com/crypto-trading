from binance.client import Client

from com_goldenthinker_trade_sessions.Session import Session


class BinanceSession(Session):
    
    def __init__(self):
        self.client = Client('xoAWbPN2iKaPiGiQZ4TiFZ0yq2AvIdO4hBw8WrjA4AsFseXNbJ09Vd6wOAc8Siaw', 'Ex3dbvWjN5DgpEm960nd2M2pFz40JuqQiOVmB61X23VZEifFH0fYu6CDo7yZBvra')
        
        