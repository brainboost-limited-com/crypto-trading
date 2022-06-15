import socket

class SocketReceive:

    def __init__(self):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.connect((socket.gethostname(), 1234))
        
        
    def listen(self,callback_function):
        while True:
            full_msg = ''
            while True:
                msg = self.s.recv(8)
                if len(msg) <= 0:
                    break
                full_msg += msg.decode("utf-8")

            if len(full_msg) > 0:
                callback_function(full_msg)