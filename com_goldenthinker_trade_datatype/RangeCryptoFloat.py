class RangeCryptoFloat:
    
    def __init__(self,a,b=None,many=None):
        if many!=None:
            self.many = many
        else:
            self.a = a
            self.b = b
        
        
    def __contains__(self,x):
        if self.b != None:
            return (x >= self.a) and (x <= self.b)
        else:
            return (x >= self.a)
        