from tinydb import Query, TinyDB


class TinyDbSession:
    def __init__(self):
        self.client = TinyDB('com_goldenthinker_trade_model/signals.json')
    
    