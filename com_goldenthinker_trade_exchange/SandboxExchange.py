
class SandboxExchange:
    
    _portfolio_sandbox = None
    
    
    @classmethod
    def portfolio(cls):
        if SandboxExchange._portfolio_sandbox is None:
            from com_goldenthinker_trade_exchange.ExchangeConfiguration import ExchangeConfiguration
            SandboxExchange._portfolio_sandbox = ExchangeConfiguration.get_default_exchange().portfolio()
            return {k:float(v) for(k,v) in SandboxExchange._portfolio_sandbox.items()}
        else:
            return SandboxExchange._portfolio_sandbox
    
    @classmethod
    def set_kv(cls,k,v):
        SandboxExchange._portfolio_sandbox[k] = v
        
        
    @classmethod
    def get_all_orders(cls):
        from com_goldenthinker_trade_database.MongoConnector import MongoConnector
        return list(MongoConnector.get_instance().get_all_orders_sandbox())