from com_goldenthinker_trade_telegram.TelegramCrawler import TelegramCrawler
from com_goldenthinker_trade_logger.Logger import Logger

# This process finds new signal channels published on the web as Telegram search feature is
# very limited. So we crawl the web using DuckDuckGo not to pay SERP



Logger.set_process_name('gt_signals_from_telegram_crawler')

# If true run risk of telegram blocking by rate limit as too many JoinRequests sent by telethon
# to crypto channels

Logger.log('signals_from_telegram_crawler started...',telegram=True)

crawler = TelegramCrawler(update_channels=False)

if crawler.crawl_for_signals():
    Logger.log("Telegram crawler finished...",telegram=True)
    
