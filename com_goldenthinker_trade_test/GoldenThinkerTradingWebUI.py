from com_goldenthinker_trade_telegram.TelegramChat import TelegramChat
from com_goldenthinker_trade_sessions.TelegramSession import TelegramSession
from com_goldenthinker_trade_telegram.TelegramCrawler import TelegramCrawler
import cherrypy
from com_goldenthinker_trade_performance import PerformanceCalculator

class GoldenThinkerTradingWebUI(object):
    
    telegram = TelegramChat()


    @cherrypy.expose
    def calculate_signals_perfornance(self):
        calculator = PerformanceCalculator()
        return calculator.calculate_signals_perfornance()
        
    @cherrypy.expose
    def obtain_older_signals_from_telegram(self):
        telegram_crawler = TelegramCrawler()
        return telegram_crawler.crawl_for_signals()
    
    
    @cherrypy.expose
    def real_time_signals_from_telegram(self):
        telegram_crawler = TelegramCrawler()
        return telegram_crawler.crawl_for_signals()
    
    
    
    
    @cherrypy.expose
    def index(self):
        return "Hello World!"



    
    
    

cherrypy.quickstart(GoldenThinkerTradingWebUI())