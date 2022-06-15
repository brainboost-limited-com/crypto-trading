import socket

class SocketSend:
    
    def __init__(self):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.bind((socket.gethostname(), 1234))
        self.s.listen(5)


    def send(self,message):
        while True:
            # now our endpoint knows about the OTHER endpoint.
            clientsocket, address = self.s.accept()
            print(f"Connection from {address} has been established.")
            clientsocket.send(bytes("Hey there!!!","utf-8"))
            clientsocket.close()