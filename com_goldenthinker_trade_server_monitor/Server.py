class Server:
    
    
    def __init__(self,user,host,passwd=None,key=None) -> None:
        if passwd==None and key==None:
            print("Server credentials are missing")
        else:
            self.user = user
            self.host = host
            self.passwd = passwd
            self.key = key
            
            
    def connect(self):
        