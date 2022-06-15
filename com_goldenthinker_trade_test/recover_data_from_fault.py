# I use just klines to recover the missing data for a symbol. 

from com_goldenthinker_trade_exchange.ExchangeConfiguration import ExchangeConfiguration
from com_goldenthinker_trade_database.MongoConnector import MongoConnector

client = ExchangeConfiguration().get_default_exchange()



def recover_data(symbol):
    mongo_connector =  MongoConnector.get_instance()
    exchange_name = client.get_exchange_name()
    collection_name = exchange_name + '_' + symbol
    mongo_connector.query_collection(collection_name=collection_name, query={})