class ServerMonitor:
    
    
    _instance = None
    
    @classmethod
    def get_instance(cls):
        if cls._instance==None:
            cls._instance = cls.__init__()
        return cls._instance
    
    
    def __init__(self) -> None:
        self.servers = []
        
    