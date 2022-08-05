import subprocess


from com_goldenthinker_trade_config.Config import Config
from com_goldenthinker_trade_exchange.Exchange import Exchange
import sys
from binance.client import Client
from binance.exceptions import BinanceAPIException, BinanceRequestException
from com_goldenthinker_trade_exchange.SandboxExchange import SandboxExchange
from com_goldenthinker_trade_model.Kline import Kline
from binance import ThreadedWebsocketManager
import time
from urllib3.exceptions import ProtocolError
from requests.exceptions import ChunkedEncodingError
from com_goldenthinker_trade_logger.Logger import Logger

from com_goldenthinker_trade_exchange.Exchange import Exchange
from os.path import exists
import os
from ratelimit import limits,sleep_and_retry
from com_goldenthinker_trade_model.Symbol import Symbol

from com_goldenthinker_trade_model_order.BuyMarketOrder import BuyMarketOrder
from com_goldenthinker_trade_model_order.SellMarketOrder import SellMarketOrder
from com_goldenthinker_trade_simulator.Simulator import Simulator
from com_goldenthinker_trade_utils.Utils import Utils
#import _thread

class BinanceExchange(Exchange):
    
    _instance = None
    _requests_sent = 0
    _exchange_name = 'binance'
    _sandbox = {}
    
    API_KEY = None
    API_SECRET = None
    
    
    _request_weights = {}
    # https://www.binance.com/en/support/announcement/f3d75a44fc7b4610b080b9c3499ed075
    

    @classmethod
    def instance(cls):
        cls._request_weights['order'] = 2
        cls._request_weights['openOrders'] = 3
        cls._request_weights['allOrders'] = 10
        cls._request_weights['orderList'] = 2
        cls._request_weights['openOrderList'] = 3
        cls._request_weights['account'] = 10
        cls._request_weights['myTrades'] = 10
        cls._request_weights['exchangeInfo'] = 10
        if cls._instance is None:
            cls._instance = cls.__new__(cls)
            # Put any initialization here.
            cls._instance.id = BinanceExchange.API_KEY
            cls._instance.secret = BinanceExchange.API_SECRET
            if (cls._requests_sent%10==0):
                cls._instance.client = None
                cls._instance.client = Client(cls._instance.id,cls._instance.secret)
            Logger.log("BinanceExchange instance created")
        return cls._instance
            
    
    @sleep_and_retry
    @limits(calls=36, period=60)
    def get_klines(self,symbol: Symbol,date_a,date_b):
        symbol_str_upper = symbol.uppercase_format()
        Logger.log("BinanceExchange request, get_klines, " + str(symbol_str_upper) + "," + str(date_a) + "," + str(date_b))
        try:            
            klines_binance = self.client.get_historical_klines(symbol_str_upper, Client.KLINE_INTERVAL_30MINUTE, date_a, date_b)
            klines = [Kline(symbol_str_upper,k) for k in klines_binance]
            self.__class__._requests_sent = self.__class__._requests_sent + 1
            return klines
        except BinanceAPIException:
            Logger.log("Symbol " + symbol_str_upper + " is not supported in Binance exchange." )

    
    def get_current_price(self,symbol: Symbol):
        symbol_str_upper = symbol.uppercase_format()
        self.__class__._requests_sent = self.__class__._requests_sent + 1
        current_price_str = self.client.get_symbol_ticker(symbol=symbol_str_upper)['price']
        Logger.log("BinanceExchange request, get_current_price, " + str(symbol_str_upper))
        return current_price_str

    
    def balance(self,symbol: Symbol,base=False):
        symbol_str_upper = symbol.uppercase_format()
        self.__class__._requests_sent = self.__class__._requests_sent + 1
        Logger.log("BinanceExchange request, balance ," + str(symbol_str_upper))
        if not base:
            return self.client.get_asset_balance(asset=symbol.get_symbol_quote_asset())['free']
        else:
            return self.client.get_asset_balance(asset=symbol.get_symbol_base_asset())['free']

    
    
    def portfolio(self):
        try:
            portfolio_data = self.client.get_account()['balances']
            portfolio_dict = dict()
            [ portfolio_dict.__setitem__(x['asset'].lower(),x['free']) for x in portfolio_data if (float(x['free'])>0) ]
            self.__class__._requests_sent = self.__class__._requests_sent + 1
            Logger.log("BinanceExchange request: portfolio ")
            if portfolio_dict == None:
                portfolio_dict = dict()
            return portfolio_dict
        except BinanceRequestException:
            Logger.log("BinanceExchange request, portfolio, BinanceRequestException ")
        except BinanceAPIException:
            Logger.log("BinanceExchange request, portfolio, BinanceRequestException ")
    
    def get_list_of_symbols(self):
        Logger.log("BinanceExchange request: get_list_of_symbols ")
        exchange_info = self.client.get_exchange_info()
        return [Symbol(s['baseAsset']+ "/" +s['quoteAsset']) for s in exchange_info['symbols']]

    
    @sleep_and_retry
    @limits(calls=12, period=60)
    def get_all_orders(self,symbol: Symbol):
        symbol_uppercase = symbol.uppercase_format()
        Logger.log("BinanceExchange request, get_all_orders ")
        if not Config.sandbox():
            self.__class__._requests_sent = self.__class__._requests_sent + 1
            return self.client.get_all_orders(symbol=symbol_uppercase, limit=10)
        else:
            from com_goldenthinker_trade_database.MongoConnector import MongoConnector
            orders_for_symbol = list(MongoConnector.get_instance().get_all_orders_sandbox(symbol=symbol,limit=10))
            from com_goldenthinker_trade_datatype.CryptoFloat import CryptoFloat
            return [BuyMarketOrder(quote_amt=CryptoFloat(Symbol(o['symbol']),o['quote_amt'])) for o in orders_for_symbol]
        

    def futures_exchange_info(self):
        Logger.log("BinanceExchange request, futures_exchange_info ")
        return self.client.futures_exchange_info()

    
    @sleep_and_retry
    @limits(calls=1200, period=1)
    def get_symbol_information(self,symbol):
        symbol_str = symbol.uppercase_format()
        symbol_uppercase_str = symbol.uppercase_format()
        from com_goldenthinker_trade_database.MongoConnector import MongoConnector
        if (MongoConnector.get_instance().check_if_symbol_in_database(symbol)) == False:
            if Logger.get_process_name()=='detect_new_symbols':
                Logger.log("BinanceExchange request found a new symbol: " + str(symbol_uppercase_str) + " adding to database: get_symbol_information",telegram=True,public=True)
            try:
                symbol_data = self.client.get_symbol_info(symbol=symbol_uppercase_str)
                symbol_data['step'] = float(symbol_data['filters'][2]['stepSize'])
                symbol_data['precision'] = symbol_data['quoteAssetPrecision']
                # filters
                
                symbol_data['min_notional'] = float(symbol_data['filters'][3]['minNotional'])
                symbol_data['min_quantity'] = float(symbol_data['filters'][2]['minQty'])
                symbol_data['max_quantity'] = float(symbol_data['filters'][2]['maxQty'])
                symbol_data['step_size'] = float(symbol_data['filters'][2]['stepSize'])
                symbol_data['tick_size'] = float(symbol_data['filters'][0]['tickSize'])
                
                # precision
                symbol_data['base_asset_precision'] = symbol_data['baseAssetPrecision']
                symbol_data['quote_precision'] = symbol_data['quoteAsset']
                symbol_data['quote_asset_precision'] = symbol_data['quoteAssetPrecision']
                symbol_data['base_comission_precision'] = symbol_data['baseCommissionPrecision']
                symbol_data['quote_comission_precision'] = symbol_data['quoteCommissionPrecision']
                
                from com_goldenthinker_trade_database.MongoConnector import MongoConnector
                MongoConnector.get_instance().insert_symbol_information(BinanceExchange._exchange_name,symbol,symbol_data)
                Logger.log("Symbol inserted into database.")
                self.__class__._requests_sent = self.__class__._requests_sent + 1
                return symbol_data
            except ConnectionResetError:
                time.sleep(69)
                Logger.log("BinanceExchange request, get_symbol_information, ConnectionResetError")
            except ProtocolError:
                time.sleep(69)
                Logger.log("BinanceExchange request, get_symbol_information, ProtocolError")
            except ConnectionError:
                time.sleep(60)
                Logger.log("BinanceExchange request, get_symbol_information, ConnectionError")   
            except ChunkedEncodingError:
                time.sleep(60)
                Logger.log("BinanceExchange request, get_symbol_information, ChunkedEncodingError")         
            self.__class__._requests_sent = self.__class__._requests_sent + 1
        else:
            Logger.log("BinanceExchange request: get_symbol_information (cached) " + "for symbol: " + str(symbol_str))
            return MongoConnector.get_instance().get_symbol_information(symbol)



    @sleep_and_retry
    @limits(calls=10, period=60)
    def futures_create_order(self,symbol=None, side=None, type=None, quantity=None):
        Logger.log("BinanceExchange request: futures_create_order " + " for symbol, " + str(symbol) + "," + str(side) + "," + str(type) + "," + str(quantity))
        self.client.futures_create_order(symbol=symbol, side=side, type=type, quantity=quantity)
        
    
    @sleep_and_retry
    @limits(calls=10, period=60)
    def create_limit_buy_order(self,symbol,qty,price):
        Logger.log("BinanceExchange request: create_limit_buy_order " + " for symbol, "  + str(symbol) + "," + str(qty) + "," + str(price))
        self.__class__._requests_sent = self.__class__._requests_sent + 1
        self.client.order_limit_buy(
            quantity=qty,
            price=price)
        
        
    @sleep_and_retry
    @limits(calls=10, period=60)    
    def create_market_limit_order(self,symbol,qty):
        Logger.log("BinanceExchange request: create_market_limit_order " + " for symbol, " + str(symbol) + str(qty))
        self.__class__._requests_sent = self.__class__._requests_sent + 1
        self.client.futures_create_order(symbol=symbol.uppercase_format(), side='BUY', type='MARKET', quantity=qty)
    
    
    
    @sleep_and_retry
    @limits(calls=10, period=60)
    def create_limit_sell_order(self,symbol: Symbol,qty,price):
        symbol_str_upper = symbol.uppercase_format()
        Logger.log("BinanceExchange request: create_limit_sell_order " + " for symbol, "  + str(symbol) + "," + str(qty) + "," + str(price))
        self.__class__._requests_sent = self.__class__._requests_sent + 1
        self.client.order_limit_sell(
            symbol=symbol.uppercase_format(),
            quantity=qty,
            price=price)

    def order_market_buy(self,symbol: Symbol,float_quantity):
        symbol_str_uppercase = symbol.uppercase_format()
        if not Config.sandbox():
            return self.client.create_order(symbol=symbol_str_uppercase,side=Client.SIDE_BUY,type=Client.ORDER_TYPE_MARKET,quantity=float_quantity)
        else:
            from com_goldenthinker_trade_datatype.CryptoFloat import CryptoFloat
            from com_goldenthinker_trade_model.Symbol import Symbol
            s = symbol
            current_portfolio = dict(SandboxExchange.portfolio())
            quote_symbol = Symbol(symbol_str_uppercase).get_symbol_quote_asset().lower()
            my_balance = float(current_portfolio[quote_symbol])
            if CryptoFloat(Symbol(symbol_str_uppercase),my_balance) > s.get_min_notional():
                Simulator.get_instance().buy(BuyMarketOrder(quote_amt=CryptoFloat(symbol=symbol_str_uppercase,float_value=float_quantity)))
                current_portfolio[quote_symbol] = float(CryptoFloat(symbol=symbol_str_uppercase,float_value=float(current_portfolio[quote_symbol])) - CryptoFloat(symbol=symbol_str_uppercase,float_value=float_quantity))
                SandboxExchange.set_kv(quote_symbol,float(current_portfolio[quote_symbol]) - float(float_quantity))
            return None
            
    
    def order_market_sell(self,sell_order: SellMarketOrder):
        symbol = sell_order.get_symbol()
        float_quantity = sell_order.get_base_qty()
        symbol_str_uppercase = symbol.uppercase_format()
        if not Config.sandbox():
            return self.client.create_order(symbol=symbol_str_uppercase,side=Client.SIDE_SELL,type=Client.ORDER_TYPE_MARKET,quantity=float_quantity)
        else:
            from com_goldenthinker_trade_datatype.CryptoFloat import CryptoFloat
            Simulator.get_instance().sell(sell_order)
            return None
    
    def get_all_tickers(self):
        self.__class__._requests_sent = self.__class__._requests_sent + 1
        return self.client.get_all_tickers()
    
    
    def subscribe_multiple_individual_symbols(self,callback=None,symbols=[]):
        try:
            streams_from_symbols_names = [(x.lower()+'@ticker') for x in symbols]
            twm = ThreadedWebsocketManager(api_key=BinanceExchange.API_KEY, api_secret=BinanceExchange.API_SECRET)
            twm.start()
            twm.start_multiplex_socket(callback=callback, streams=streams_from_symbols_names)
            twm.join()
        except:
            Logger.log("Error socket multiple symbols")
            
    
    def subscribe_all_symbols_stream(self,callback=None):
        try:
            twm = ThreadedWebsocketManager(api_key=BinanceExchange.API_KEY, api_secret=BinanceExchange.API_SECRET)
            twm.start()
            twm.start_multiplex_socket(callback=callback, streams=['!ticker@arr'])
            twm.join()
        except:
            Logger.log("Error subscribing to all symbols stream")
            sys.exit()
    
    def get_exchange_name(self):
        return BinanceExchange._exchange_name
    
        
    def example(self):
        symbol = 'BNBBTC'

        twm = ThreadedWebsocketManager(api_key=BinanceExchange.API_KEY, api_secret=BinanceExchange.API_SECRET)
        # start is required to initialise its internal loop
        twm.start()

        def handle_socket_message(msg):
            print(msg)

        #twm.start_kline_socket(callback=handle_socket_message, symbol=symbol)

        # multiple sockets can be started
        #twm.start_depth_socket(callback=handle_socket_message, symbol=symbol)

        # or a multiplex socket can be started like this
        # see Binance docs for stream names
        streams = ['bnbbtc@ticker']
        twm.start_multiplex_socket(callback=handle_socket_message, streams=streams)

        twm.join()
        

    def subscribe_to_local_datasource_ticker(self,callback=None,interval=Config.get('kline_interval_min')):



        def execute(command):
            try:
                batcmd=command.split(' ')
                return subprocess.run(batcmd, capture_output=True).stdout.decode('UTF-8')
                #return str(subprocess.check_output(batcmd, shell=True,text=True))
            except:
                Logger.log("Error executing zip commmand :" + str(command),telegram=True)

        if callback != None:

            Logger.log('Extracting .zip file to obtain csv')
            storage_dir = 'D:\/historical\/binance\/'

            from com_goldenthinker_trade_exchange.ExchangeConfiguration import ExchangeConfiguration
            list_of_symbols = ExchangeConfiguration.get_default_exchange().get_list_of_symbols()
        
            Logger.log('Starting the local kline to tick streaming process.')
            for s in list_of_symbols:
                symbol_data_directory = storage_dir + 'binance-public-data/python/data/spot/monthly/klines/' + str(s) + '/' + interval + '/'
                files_list_str = Utils.execute(command='ls ' + symbol_data_directory)
                files = files_list_str.split('\n')
                for f in files:
                    if '.zip' in f:

                        file_path = symbol_data_directory+f
                        csv_file_name = file_path.split('.')[:-1][0] + '.csv'

                        if not exists(csv_file_name):
                            Utils.execute('unzip '+file_path)
                            Utils.execute('mv '+ csv_file_name.split('/')[-1] + ' ' + symbol_data_directory)
                            os.remove(file_path)
                            Logger.log("Unzipped file "+file_path.split('/')[-1])
                        else:
                            Logger.log("File " + file_path.split('/')[-1] + " already exists generating ticks.")

                        csv_file_content = open(csv_file_name, 'r')
                        csv_file_lines = csv_file_content.readlines()

                        co = 0
                        le = len(csv_file_lines)
                        for l in csv_file_lines:
                            Logger.log('Processing kline : '+ str(co) + ' of ' + str(le) + ' kline: ' +l)
                            kline = Kline(s,l.split(','))
                            tick = kline.to_tick('5m')
                            callback(data=tick)
                            co = co + 1
                        
                        rem_command = 'rm ' + str(symbol_data_directory+csv_file_name)
                        Logger.log(rem_command)
                        Utils.execute(rem_command)
                    
                        Logger.log('File ' + str(csv_file_name) + ' has been tick streamed to the system and stored in database in sequences rise/drop. ')

                Logger.log('Symbol '+ str(s) + ' has been processed.') 

            Logger.log('Process completed successfully.')




