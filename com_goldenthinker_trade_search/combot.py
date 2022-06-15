from urllib.error import URLError
from urllib.request import Request, urlopen
import mechanize
from bs4 import BeautifulSoup
import urllib.parse
import re
from random import choice
from tinydb import Query, TinyDB
import validators
import json

def extract_telegram_channels(url):
    req = Request(
        url, 
        data=None, 
        headers={
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'
        }
    )

    page = urlopen(req)
    html = page.read().decode("utf-8")
    json_data = json.loads(html)
    results = []
    for c in json_data:
        results.append('https://t.me/' + str(c['u']))
    return results



client = TinyDB('com_goldenthinker_trade_search/telegram_channels.json')


limit = -20
offset = 0
for i in range(1,3194):
    limit = limit + 20
    offset = offset + 20
    url = "https://www.combot.org/api/chart/all?limit=" + str(limit) + "&offset=" + str(offset) + "&q=investc"

    current_link = urllib.parse.unquote(url)
    if validators.url(current_link):
        try:
            print("Extract signal channels from website " + current_link)
            channels_found_in_website = extract_telegram_channels(current_link)
            print("Done")
            for c in channels_found_in_website:
                channel_exists = Query()
                if len(client.search(channel_exists.channel==c)) == 0:
                    client.insert({'channel': c})
                    print("Inserted: " + c)
        except URLError:
            print("Website " + current_link + " is not good. Continuing with others..")


