from com_goldenthinker_trade_utils.Date import Date
from com_goldenthinker_trade_model_parsers.SignalParser2 import SignalParser2

signal1 = """New Trading Signal @ 2021-07-14 08:00 (UTC)
Symbol: WANUSDT
Signal: BUY
Buy @: ~0.52090000
Candle size: 4h (2021-07-14 08:00 UTC)
Exchange: Binance - Earn 10% comission @ registration
TradingView: Analyze WANUSDT - Total Market CAP
------------------------------------------------------
24h Volume: 846680.76 USDT ($1,565,357 WAN)
24h Change: -8.45% (-0.04810000)
Market Cap: $100,695,877
Ranking: 271
👉 Check our Results Channel
👉 Subscribe for our VIP Channels"""

signal2 = """New Trading Signal @ 2021-07-14 23:00 (UTC)
Symbol: SANDUSDT
Signal: STRONG SELL
Sell @: ~0.59261000
Candle size: 1h (2021-07-14 23:00 UTC)
Exchange: Binance - Earn 10% comission @ registration
TradingView: Analyze SANDUSDT - Total Market CAP
------------------------------------------------------
24h Volume: 157545561.08 USDT ($316,101,419 SAND)
24h Change: 33.88% (0.14986000)
Market Cap: $405,333,895
Ranking: 108
👉 Check our Results Channel
👉 Subscribe for our VIP Channels"""


signal3 = """New Trading Signal @ 2021-07-15 01:01 (UTC)
Symbol: CHZBTC
Signal: SELL
Sell @: ~0.00000770
Candle size: 1h (2021-07-15 01:00 UTC)
Exchange: Binance - Earn 10% comission @ registration
TradingView: Analyze CHZBTC - Total Market CAP
------------------------------------------------------
24h Volume: 263.81 BTC ($35,694,287 CHZ)
24h Change: 7.09% (0.00000051)
Market Cap: $1,464,434,648
Ranking: 58
👉 Check our Results Channel
👉 Subscribe for our VIP Channels"""

signal4 = """Exchange: Binance
#BANDUSDT

Trade Type: short position

Entry zone 6.20 - 6.00

Amount: 3% from deposit

Leverage x5


Target:
1) 5.80
2) 5.65
3) 5.30

Stop 6.35"""

my_signal = SignalParser2(unstructred_text=signal4,timestampt=Date().now_yyyymmdd_str(),channel='testing_channel').parse()
print(str(my_signal))

