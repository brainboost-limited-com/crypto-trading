from com_goldenthinker_trade_exchange.ExchangeConfiguration import ExchangeConfiguration
from com_goldenthinker_trade_logger.Logger import Logger
from com_goldenthinker_trade_model.Symbol import Symbol


# Thia process executes every 5 hours looking for new symbol opportunities in the exchange
# as new symbols always have huge spike at first

Logger.set_process_name('gt_detect_new_symbols')

exchange = ExchangeConfiguration.get_default_exchange()
Logger.log("Updating database of symbols.")

updated_symbols = exchange.get_list_of_symbols()

for s in updated_symbols:
    exchange.get_symbol_information(symbol=Symbol(s))

Logger.log('new symbols have been added to the database...')



