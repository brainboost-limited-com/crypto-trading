import sys

if 'com_goldenthinker_trade_model_parsers.SignalParserNew' not in sys.modules:
    from com_goldenthinker_trade_model_parsers.SignalParserNew import SignalParserNew
from tinydb.database import TinyDB
from tinydb.queries import Query, where




class TinyDbConnector:
    
    _instance_for_channels = None
    _instance_for_signals = None    
    _instance_for_sequences = None
    
    def __init__(self):
        pass
    
    
    @classmethod
    def instance_for_sequences(cls,symbol):
        if cls._instance_for_sequences is None:
            cls._instance_for_sequences = cls.__new__(cls)
            # Put any initialization here.
            cls._instance_for_sequences.db = TinyDB('storage/sequences/' + symbol + '.json')
        return cls._instance_for_sequences
    

    def insert_sequence(self,sequence=None,symbol=None):
        my_id = Query()
        if self.__class__._instance_for_sequences.instance_for_sequences(symbol).db.get(my_id.id == sequence['id'])==None:
            self.__class__._instance_for_sequences.instance_for_sequences(symbol).db.insert(sequence)
    
    
    
    @classmethod
    def instance_for_channels(cls):
        if cls._instance_for_channels is None:
            cls._instance_for_channels = cls.__new__(cls)
            # Put any initialization here.
            cls._instance_for_channels.db = TinyDB('storage/telegram_channels.json')

        return cls._instance_for_channels

    @classmethod
    def get_channels(cls):
        channels = cls._instance_for_channels.db.all()
        return channels
    
    @classmethod
    def remove_channel(cls,channel):
        cls._instance_for_channels.instance_for_channels().db.remove(where('channel')==channel)


    @classmethod
    def instance_for_signals(cls):
        if cls._instance_for_signals is None:
            cls._instance_for_signals = cls.__new__(cls)
            # Put any initialization here.
            cls._instance_for_signals.db = TinyDB('storage/signals.json')

        return cls._instance_for_signals
            
    
    
    def get_signals(self):
        signals_from_db = self.__class__._instance_for_signals.instance_for_signals().db.all()
        signals = [SignalParserNew(unstructred_text=str(x),timestampt=None,channel=None).parse() for x in signals_from_db]
        return signals
    
    
    def save_signal(self,signal):
        try:
            my_id = Query()
            if self.__class__._instance_for_signals.instance_for_signals().db.get(my_id.id == signal.generate_id())==None:
                self.__class__._instance_for_signals.instance_for_signals().db.insert(signal.to_dict())
            #else:
            #    print("Updating signal id num: " + signal.generate_id() + "...")
            #    self.__class__._instance_for_signals.instance_for_signals().remove_signal(signal)
            #    self.__class__._instance_for_signals.instance_for_signals().db.insert(signal.to_dict())
        except KeyError:
            print("KeyError: symbol does not exist, this seems not to be a signal, continuing ...")
    
    def remove_signal(self,signal):
        self.__class__._instance_for_signals.instance_for_signals().db.remove(where('id')==signal.generate_id())
    
    
    def channels_processed_so_far(self):
        q = Query()
        texts = [q.get('channel').split('/')[-1] for q in self.__class__.instance_for_channels().db.search(q.channel.exists())]
        if len(texts) > 0:
            print("Continue processing from the last channel " + texts[-1])
        return texts
        