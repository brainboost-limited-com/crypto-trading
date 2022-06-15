from abc import ABCMeta
from multiprocessing.connection import Client


class Session:
      
    
    def __init__(self, name: str, client: object) -> None:
        self.client = client
        
    def get_client(self) -> object:
        return self.client