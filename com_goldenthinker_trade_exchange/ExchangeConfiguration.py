from com_goldenthinker_trade_exchange.BitrexExchange import BitrexExchange
from com_goldenthinker_trade_exchange.CoinBaseExchange import CoinBaseExchange
from com_goldenthinker_trade_exchange.CryptoExchange import CryptoExchange
from com_goldenthinker_trade_exchange.GeminiExchange import GeminiExchange
from com_goldenthinker_trade_exchange.KrakenExchange import KrakenExchange
from com_goldenthinker_trade_exchange.KukoinExchange import KukoinExchange
from com_goldenthinker_trade_exchange.BinanceExchange import BinanceExchange
from com_goldenthinker_trade_config.Config import Config




class ExchangeConfiguration:
    
    
    # Configure default exchange here
    
    _default_exchange = 'binance'
    _credentials_dictionary = {
        'binance' : [Config.get('exchange_api_credential_key_1'),
                     Config.get('exchange_api_credential_secret_1')],
        'coinbase' : [Config.get('exchange_api_credential_name_2'),
                    Config.get('exchange_api_credential_key_2'),
                    Config.get('exchange_api_credential_secret_2')],
        'kraken'   : [Config.get('exchange_api_credential_name_3')],
        'bitrex' : [],
        'crypto': [],
        'gemini' : []
        
    }
    
    
    @classmethod
    def get_default_exchange(cls):
        return cls.get_exchange_by_name(name=cls._default_exchange)
    
    @classmethod
    def get_default_exchange_name(cls):
        return cls._default_exchange
    
    
    @classmethod
    def get_exchange_by_name(cls,name='binance'):
        do = f"get_{name}_exchange"
        if hasattr(cls, do) and callable(func := getattr(cls, do)):
            return func()
    
    
    @classmethod
    def get_binance_exchange(cls):
        BinanceExchange.API_KEY = cls._credentials_dictionary['binance'][0]
        BinanceExchange.API_SECRET = cls._credentials_dictionary['binance'][1]
        return BinanceExchange.instance()
    
    @classmethod
    def get_coinbase_exchange(cls):
        CoinBaseExchange.API_KEY = cls._credentials_dictionary['coinbase'][0]
        CoinBaseExchange.API_SECRET = cls._credentials_dictionary['coinbase'][1]
        CoinBaseExchange.PWD = cls._credentials_dictionary['coinbase'][2]
        return CoinBaseExchange.instance()
            
    
    @classmethod
    def get_bitrex_exchange(cls):
        return BitrexExchange.instance()

    @classmethod
    def get_crypto_exchange(cls):
        return CryptoExchange.instance()

    @classmethod
    def get_gemini_exchange(cls):
        return GeminiExchange.instance()

    @classmethod
    def get_kraken_exchange(cls):
        return KrakenExchange.instance()
    
    @classmethod
    def get_kukoin_exchange(cls):
        return KukoinExchange.instance()
    
    @classmethod
    def get_kraken_exchange(cls):
        return KrakenExchange.instance()
