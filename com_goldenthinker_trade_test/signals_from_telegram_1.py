from com_goldenthinker_trade_telegram.TelegramCrawler import TelegramCrawler



# If true run risk of telegram blocking by rate limit as too many JoinRequests sent by telethon
# to crypto channels
crawler = TelegramCrawler(update_channels=False)

if crawler.crawl_for_signals():
    print("Telegram crawler finished...")
    
