from com_goldenthinker_trade_monitor.TickerSocket import TickerSocket
from com_goldenthinker_trade_model.Symbol import Symbol
from com_goldenthinker_trade_monitor.TickerSocket import TickerSocket
from com_goldenthinker_trade_monitor.SymbolMonitor import SymbolMonitor


btc_usdt_monitor = SymbolMonitor(Symbol('btc/usdt'))
#eth_usdt_monitor = SymbolMonitor(Symbol('eth/usdt'))
#yfi_usdt_monitor = SymbolMonitor(Symbol('yfi/usdt'))

my_ticker = TickerSocket.instance()
my_ticker.add_listener_monitor(btc_usdt_monitor)
#my_ticker.add_listener_monitor(eth_usdt_monitor)
#my_ticker.add_listener_monitor(yfi_usdt_monitor)

my_ticker.start()