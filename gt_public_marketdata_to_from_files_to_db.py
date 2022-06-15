
from com_goldenthinker_trade_exchange.ExchangeConfiguration import ExchangeConfiguration

from com_goldenthinker_trade_datasource_network.TickerSocketAllSymbols import TickerSocketAllSymbols

from com_goldenthinker_trade_log.Logger import Logger

Logger.set_process_name = 'gt_public_marketdata_to_from_files_to_db'


local_ticker = TickerSocketAllSymbols(exchange=ExchangeConfiguration.get_default_exchange(),local_source=True)

local_ticker.start()