
from datetime import datetime, timedelta
import certifi
from numpy import where
from pymongo.collection import ReturnDocument
from sshtunnel import SSHTunnelForwarder
import pymongo
from com_goldenthinker_trade_model.Symbol import Symbol
from com_goldenthinker_trade_model_order.Order import Order
from com_goldenthinker_trade_logger.Logger import Logger
import sshtunnel

from com_goldenthinker_trade_model_signals.Signal import Signal
from pymongo.write_concern import WriteConcern
from com_goldenthinker_trade_config.Config import Config
import ssl


class MongoConnector:
    
    _instance = None
    _timezone_server_offset_in_minutes = 0
    _config = None
    
    @staticmethod
    def get_instance(atlas=None):
        if MongoConnector._config == None:
            MongoConnector._config = Config.read_config()
            
        if atlas==None:
            if MongoConnector._instance == None:
                MongoConnector()
        else:
            if MongoConnector._instance == None:
                MongoConnector(atlas=True)
        return MongoConnector._instance
    
    def __init__(self,atlas=None):
        if atlas==None:
            if MongoConnector._instance != None:
                raise Exception("This class is a singleton!")
            else:
                self.MONGO_DB = MongoConnector._config.get('service_database_name_1_2')
                if MongoConnector._config.get('service_use_ssh_tunnel_1_2') == 'yes':
                    self.MONGO_HOST = MongoConnector._config.get('internal_ip_1')
                    #self.PRIVATE_KEY = MongoConnector._config.get('node_cert_1')
                    self.SERVER_USER = MongoConnector._config.get('service_user_1_1')
                    self.PASSWORD = MongoConnector._config.get('service_pass_1_1')
                    
                    # define ssh tunnel
                    self.server = SSHTunnelForwarder(
                        ssh_host=self.MONGO_HOST,
                        ssh_username=self.SERVER_USER,
                        #ssh_pkey=self.PRIVATE_KEY,
                        ssh_password=self.PASSWORD,
                        remote_bind_address=(MongoConnector._config.get('service_exposure_1_2'), int(MongoConnector._config.get('service_port_1_2')))
                    )
                    sshtunnel.TUNNEL_TIMEOUT = 10.0
                
                    # start ssh tunnel
                    self.server.start()
                    #connection = pymongo.MongoClient(MongoConnector._config.get('internal_ip_1'), self.server.local_bind_port,tls=True,tlsCertificateKeyFile='lets-encrypt-r3.pem')
                    connection = pymongo.MongoClient(MongoConnector._config.get('service_exposure_1_2'),self.server.local_bind_port)
                    self.db = connection.get_database(self.MONGO_DB,write_concern=WriteConcern(w=0))
                    MongoConnector._instance = self
                    Logger.log("mongodb connected ssh tunnel : 127.0.0.1 " + str(self.server.local_bind_port) )
                    
                else:
                    self.MONGO_HOST = MongoConnector._config.get('service_bind_1_2')
                    #CONNECTION_STRING = "mongodb://" + MongoConnector._config.get('service_bind_1_2') + ":" + MongoConnector._config.get('service_port_1_2') + "/" + self.MONGO_DB
                    #connection = pymongo.MongoClient(MongoConnector._config.get('service_bind_1_2'),int(MongoConnector._config.get('service_port_1_2')),username=MongoConnector._config.get('service_user_1_2'), password=MongoConnector._config.get('service_pass_1_2'))
                    #connection = pymongo.MongoClient(CONNECTION_STRING,tls=True,tlsCertificateKeyFile='lets-encrypt-r3.pem')
                    
                    #connection = pymongo.MongoClient('mongodb://' + MongoConnector._config.get('service_user_1_2') + ':' + MongoConnector._config.get('service_pass_1_2')+'@' + MongoConnector._config.get('service_bind_1_2') + ':' + MongoConnector._config.get('service_port_1_2')+'/')
                    connection = pymongo.MongoClient('mongodb://' + str(Config.get('service_bind_1_2')) + ':' + str(Config.get('service_port_1_2')))
                    
                    self.db = connection[self.MONGO_DB]
                    MongoConnector._instance = self
                    Logger.log("mongodb direct connection :" + str(MongoConnector._config.get('service_bind_1_2')))
        else:    
            if MongoConnector._instance != None:
                raise Exception("This class is a singleton!")
            else:
                
                import certifi
                ca = certifi.where()
                print("connect to " + Config.get('service_connection_url_2'))
                if (Config.get('service_use_ssl_1_2'))=='yes':
                    connection = pymongo.MongoClient(Config.get('service_exposure_1_2'),ssl=True,ssl_cert_reqs=ssl.CERT_NONE)
                else:
                    connection = pymongo.MongoClient(Config.get('service_exposure_1_2'))
                self.db = connection[Config.get("service_database_name_1_2")]
                MongoConnector._instance = self
                Logger.log("Connected to DigitalOcean")
            
            
        
    def query_collection(self,collection_name=None, query={}):
        data = self.db[collection_name].find(query, no_cursor_timeout=True)
        Logger.log("query_collection: " + str(collection_name) + " " + str(query) + " results: " + str(data.count()))
        return data
    
    def list_collection_names(self):
        return self.db.collection_names()
    
    
    def drop_collection(self,name: str):
        self.db[name].drop()
    

    
    
    # Inserting sequences into the same document from a collection all the time end up hitting the MongoDB
    # 16 MB target when the document is updated by adding the sequence to the symbol's tick_sequences_array
    # This means that using the first approach one collection per symbol will never generate documents larger
    # than 16 MB, plus gives the freedom to the split symbols into multiple instances.
    
    def insert_sequence_into_new_document_or_push_to_existing(self,exchange=None,sequence=None,symbol=None):
        Logger.log("insert_sequence_into_new_document_or_push_to_existing: " + str(sequence) + " " + str(symbol))
        if exchange==None:
            from com_goldenthinker_trade_exchange.ExchangeConfiguration import ExchangeConfiguration
            exchange = ExchangeConfiguration.get_default_exchange_name()
        
        updated_doc = self.db['ticks'].find_one_and_update(filter={'exchange': exchange,'symbol': symbol }, 
                                            update={'$addToSet': {'tick_sequences': dict(sequence)}},sort=None,upsert=True,
                                            return_document= ReturnDocument.AFTER, no_cursor_timeout=True)
        Logger.log("sequence " + str(sequence) + " updated-inserted successfully for symbol: " + str(symbol)  )
        return updated_doc
    
    
    def create_unique_index_with_new_collection(self,collection_name: str,unique_field_name=None):
        colections = self.list_collection_names()
        if not collection_name in colections:
            self.db.create_collection(collection_name)
            self.db[collection_name].create_index([(unique_field_name,pymongo.ALL)],unique=True)
    
    
    def insert_test(self,number: Order):
        doc_id = self.db['test'].insert_one(number).inserted_id
        return doc_id
    
    
    
    def insert_signal_performance(self,performance):
        Logger.log("insert_signal_performance: " + str(performance['signal_id']))
        doc_id = self.db['signal_performance'].insert_one(dict(performance)).inserted_id
        if MongoConnector._config['service_insert_check_1_2'] == 'yes':
            check_if_insert_worked = self.query_collection('signal_performance',{'_id' : doc_id}).count() > 0
            if check_if_insert_worked == False:
                Logger.log("insert_signal_performance is not working on MongoDB for doc_id " + str(doc_id),telegram=True )
            #doc_id = self.db['signal_performance'].insert_one(dict(performance))
        Logger.log("innserted  " + str(doc_id) + "inserted: " + str(performance))
    
    
    def insert_order(self,order: Order):
        Logger.log("insert_order: " + str(order.generate_hash_id()))
        doc_id = self.db['orders'].insert_one(order).inserted_id
        if MongoConnector._config['service_insert_check_1_2'] == 'yes':
            check_if_insert_worked = self.query_collection('orders',{'_id' : str(doc_id)}).count() > 0
            if check_if_insert_worked == False:
                Logger.log("insert_order is not working on MongoDB for doc_id " + str(doc_id),telegram=True )
                quit()
            
        Logger.log("inserted_order: " + str(order.generate_hash_id()))
    

    def insert_sequence(self,sequence=None,symbol=None,exchange=None):
        Logger.log("insert_sequence: " + str(sequence) + " " + str(symbol) + " from exchange " + str(exchange))
        doc_id = (self.db[str(exchange)+'_'+symbol].insert_one(dict(sequence))).inserted_id
        if MongoConnector._config['service_insert_check_1_2'] == 'yes':
            check_if_insert_worked = self.query_collection((str(exchange)+'_'+symbol),{'_id' : str(doc_id)}).count() > 0
            if check_if_insert_worked == False:
                Logger.log("insert_sequence is not working on MongoDB for doc_id " + str(doc_id),telegram=True )
                quit()
        Logger.log("inserted_sequence " + str(sequence) + " inserted successfully for symbol: " + str(symbol) + " with id: " + str(doc_id) )
        
    def insert_symbol_information(self,exchange_name: str,symbol: Symbol,doc):
        symbol_str = symbol.uppercase_format()
        Logger.log("insert_symbol_information," + str(exchange_name) + "," + str(symbol_str))
        symbol_doc = dict(doc)
        symbol_doc['exchange'] = str(exchange_name)
        symbol_doc['symbol'] = symbol_str
        doc_id = (self.db[str(exchange_name)].insert_one(dict(symbol_doc))).inserted_id
        if MongoConnector._config['service_insert_check_1_2'] == 'yes':
            check_if_insert_worked = self.query_collection(str(exchange_name),{'_id' : doc_id}).count() > 0
            if check_if_insert_worked == False:
                Logger.log(str(exchange_name) + " insert is not working on MongoDB for doc_id " + str(doc_id),telegram=True )
                quit()
        
        Logger.log("insert_symbol_information, " + str(exchange_name) + "," + str(symbol_str) + "," + str(doc_id) + ",COMPLETED")

    def check_if_symbol_in_database(self,symbol: Symbol):
        symbol_str = symbol.uppercase_format()
        from com_goldenthinker_trade_exchange.ExchangeConfiguration import ExchangeConfiguration
        return (self.query_collection(collection_name=ExchangeConfiguration.get_default_exchange_name(),query={'symbol': symbol_str}).count()>0)
        
    def get_symbol_information(self,symbol: Symbol):
        symbol_str = symbol.uppercase_format()
        from com_goldenthinker_trade_exchange.ExchangeConfiguration import ExchangeConfiguration
        return (self.query_collection(collection_name=ExchangeConfiguration.get_default_exchange_name(),query={'symbol': symbol_str})).next()
    
    def get_channels(self):
        return self.query_collection(collection_name='channels',query={})



    def remove_channel(cls,channel: str):
        cls._instance_for_channels.instance_for_channels().db.remove(where('channel')==channel)

    def get_signals(self):
        return self.query_collection('signals',query={})
        
    def save_signal(self,signal: Signal):
        try:
            self.db['signals'].insert_one(signal)
        except KeyError:
            Logger.log("KeyError: symbol does not exist, this seems not to be a signal, continuing ...")
    
    def remove_signal(self,signal: Signal):
        self.db['signals'].remove(signal)
    
    def save_order(self,order: Order):
        try:
            self.db['orders'].insert_one(order.to_dict())
        except KeyError:
            Logger.log("KeyError: cannot insert order to the Simulator ...")
    
        
    def find_order(self,order_hash: str):
        res = list(self.query_collection('orders',query={'hash_id': order_hash}))
        if len(res)>0:
            return list(self.query_collection('orders',query={'hash_id': order_hash}))[0]
        else:
            return None
        
        
    def delete_order(self,order: Order):
        #self.db['orders'].delete_one({'hash_id': order_hash})
        order.set_disabled()
        order.save()
    
    def best_opportunity(self,since):
        names = self.list_collection_names()
        for collection in names:
            self.list_collection_names(collection_name=collection,query={})
            
    def get_latest_docs_within_last_minutes_for_symbol(self,exchange=None,symbol='',minutes=60,collection_name=''):
        if collection_name=='':
            collection_name = str(exchange)+'_'+str(symbol)
        #to_filter_by_date = list(self.query_collection(collection_name=collection_name,query={ "timestampt": {"$gt": ("new Date(ISODate().getTime() - 1000 * 60 * 60 " + "*" + " " + str(minutes+MongoConnector._timezone_server_offset_in_minutes) + ")") } }))
        to_filter_by_date = list(self.query_collection(collection_name=collection_name,query={ "timestampt": {"$gt":  (datetime.utcnow() - timedelta(minutes=minutes)) }  }))

        return to_filter_by_date




        
    def get_all_data_in_the_last_minutes_for_all_symbols(self,exchange='binance',minutes=60):
        names = self.list_collection_names()
        data = []
        for c in names:
            if '_' in c:
                symbol_data = dict()
                symbol_data['symbol'] = c
                symbol_data['data'] = self.get_latest_docs_within_last_minutes_for_symbol(minutes=minutes,collection_name=c)
                data.append(symbol_data)
        return data
    
    def average_drop_rise(self,symbol: Symbol):
        symbol_str = symbol.uppercase_format()
        try:
            from com_goldenthinker_trade_exchange.ExchangeConfiguration import ExchangeConfiguration
            sequence_name = ExchangeConfiguration.get_default_exchange_name()+"_"+symbol_str
            avg_rise_drop_result = list(self.db[sequence_name].aggregate([{'$group': {'_id':'$type', 'avg_len': {'$avg':"$len"} } }]))
            avg_rise_drop_delta_sum = list(self.db[sequence_name].aggregate([{'$group': {'_id':'$type', 'avg_delta_sum': {'$avg':"$delta_sum"} } }]))
            return (avg_rise_drop_result[0]['avg_len'],avg_rise_drop_result[1]['avg_len'],avg_rise_drop_delta_sum[0]['avg_delta_sum'],avg_rise_drop_delta_sum[1]['avg_delta_sum'])
        except Exception as e:
            return (0,0,0,0)


    def drop_rise_stats(self,symbol=None):
        minago = int(Config.get('invest_interval_minutes'))
        try:
            from com_goldenthinker_trade_exchange.ExchangeConfiguration import ExchangeConfiguration
            sequence_name = ExchangeConfiguration.get_default_exchange_name()+"_"+symbol.uppercase_format()
            
            min_ago = { "$match": { "timestampt": {"$gt": (datetime.utcnow() - timedelta(minutes=minago)) } }}
            
            
            seq_stats = dict()
            seq_stats['max_delta_rise_drop'] = list(self.db[sequence_name].aggregate([min_ago,{'$group': {'_id':'$type', 'max_delta': {'$max': {'$abs':"$analysis.biggest_delta"} }} }]))


            seq_stats['min_delta_rise_drop'] = list(self.db[sequence_name].aggregate([min_ago,{'$group': {'_id':'$type', 'min_delta': {'$min': {'$abs':"$analysis.smallest_delta"} }} }]))
            
            
            seq_stats['avg_delta_time_rise_drop']  = list(self.db[sequence_name].aggregate([min_ago,{'$group': {'_id':'$type', 'avg_delta_time': {'$avg':"$analysis.average_delta_time"} } }]))
            seq_stats['max_delta_time_rise_drop']  = list(self.db[sequence_name].aggregate([min_ago,{'$group': {'_id':'$type', 'max_delta_time': {'$max':"$analysis.max_delta_time"} } }]))
            seq_stats['min_delta_time_rise_drop']  = list(self.db[sequence_name].aggregate([min_ago,{'$group': {'_id':'$type', 'min_delta_time': {'$min':"$analysis.average_delta_time"} } }]))
            
            # We take empirically the proportion of rises and drops , lets say per each 2 rises there is 1.94 drops in average in the last minutes 
            # Per each rise delta_sum is lets say 35.93 , per each drop in average -34.51 
            rises_vs_drops_empirically = list(self.db[sequence_name].aggregate([min_ago,{'$group': {'_id':'$type', 'avg_len': {'$avg':"$len"} } }]))
            seq_stats['amount_of_drops_per_rises'] = rises_vs_drops_empirically[0]
            seq_stats['amount_of_rises_per_drops'] = rises_vs_drops_empirically[1]
            
            delta_sum_rise_vs_drop = list(self.db[sequence_name].aggregate([min_ago,{'$group': {'_id':'$type', 'avg_delta_sum': {'$avg':"$delta_sum"} } }]))
            seq_stats['delta_sum_of_drops'] = delta_sum_rise_vs_drop[0]
            seq_stats['delta_sum_of_rises'] = delta_sum_rise_vs_drop[1]
            
            return seq_stats
        except:
            return None
        
        
    def get_all_orders_sandbox(self,symbol=None,limit=10):   
        if symbol is not None:
            symbol_str = symbol.uppercase_format()
            return self.query_collection(collection_name='orders',query={'symbol':symbol_str,'status':'OPEN'})
        else:
            from com_goldenthinker_trade_model_order.BuyMarketOrder import BuyMarketOrder
            from com_goldenthinker_trade_model_order.SellMarketOrder import SellMarketOrder
            dicts_from_db = list(self.query_collection(collection_name='orders',query={'side':'BUY','status':'OPEN'}))
            return ([BuyMarketOrder(from_dict_value=o) for o in dicts_from_db if o['side']=='BUY'] + [SellMarketOrder(from_dict_value=o) for o in dicts_from_db if o['side']=='SELL'])
    
    
    def insert_logline(self,logline=None):
        if logline!=None:
            parts = logline.split(',')            
            logline_to_doc = {
                'log_id' : str(parts[0]),
                'process_name' : str(parts[1]),
                'timestamp' : str(parts[2]),
                'code_line_number' : str(parts[3]),
                'log_message' : str(parts[4]),
                'time_delta' : str(parts[5])

            }
            self.db['logger'].insert_one(logline_to_doc)