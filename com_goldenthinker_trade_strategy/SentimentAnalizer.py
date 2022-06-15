from com_goldenthinker_trade_logger.Logger import Logger
from urllib.error import URLError
from urllib.request import Request, urlopen
import mechanize
from bs4 import BeautifulSoup
import urllib.parse
import re
from random import choice
from tinydb import Query, TinyDB
import validators
from com_goldenthinker_trade_exchange.ExchangeConfiguration import ExchangeConfiguration


class SentimentAnalizer:
    
    def __init__(self):
        self.browser = mechanize.Browser()
        self.browser.set_handle_robots(False)

        self.user_agent = [('User-agent',
             'Mozilla/5.0 (X11;U;Linux 2.4.2.-2 i586; en-us;m18) Gecko/200010131 Netscape6/6.01'
        )]
        self.browser.addheaders=self.user_agent
        self.currencies = ExchangeConfiguration.get_default_exchange().get_list_of_symbols()
     
     
     
    def extract_positive_keywords(symbol):
        
        
        
        
        
        
        
    def extract_negative_keywords(symbol):
        
         
     
        
    
    def search(self):
        keywords = []
        for each_currency in self.currencies:
            keywords.append(each_currency)
        
            for q in keywords:
                base_url = "http://duckduckgo.com/html/?q="
                query_url = base_url + q
                visit_link = urllib.parse.unquote(query_url)
                page = self.browser.open(visit_link)


                source_code = page.read()
                results = []
                results.extend(self.browser.links())
                for i in results:
                    current_link = urllib.parse.unquote(i.url).split('&rut')[0][25:]
                    if validators.url(current_link):
                        try:
                            Logger.log("Extract signal channels from website " + current_link)
                            channels_found_in_website = extract_telegram_channels(current_link)
                            Logger.log("Done")
                            for c in channels_found_in_website:
                                channel_exists = Query()
                                if len(self.client.search(channel_exists.channel==c)) == 0:
                                    self.client.insert({'channel': c})
                                    Logger.log("Inserted: " + c)
                        except URLError:
                            Logger.log("Website " + current_link + " is not good. Continuing with others..")
                results = []
        