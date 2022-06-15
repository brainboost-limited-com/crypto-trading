
from com_goldenthinker_trade_logger.Logger import Logger
Logger.set_process_name(name='gt_monitor_all_symbols')

from com_goldenthinker_trade_datasource.DataSourceManager import DataSourceManager





Logger.log("All symbols monitoring starting...",telegram=True)

DataSourceManager.get_data_source('gt_monitor_all_symbols').start()