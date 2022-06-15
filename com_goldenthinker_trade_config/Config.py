class Config:
    
    _conf = {}
    
    @classmethod
    def read_config(cls):
        content = ''
        with open('global.config') as f:
            content = f.readlines()
        
        for l in content:
            if len(l) > 3:
                if not '#' in l:
                    try:
                        a = l.split('=')[0].replace(' ','').replace('  ','').replace('\n','')
                        b = l.split('=')[1].replace(' ','').replace('  ','').replace('\n','')
                    except:
                        print(a)
                    cls._conf[a] = b
        return cls._conf
    
    
    @classmethod
    def get(cls,k):
        if cls._conf=={}:
            cls.read_config()
        return cls._conf[k]
            
    @classmethod
    def sandbox(cls):
        return cls.get(k='mode')=='sandbox'
        