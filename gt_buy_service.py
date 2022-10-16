from com_goldenthinker_trade_logger.Logger import Logger
Logger.set_process_name('gt_buy_service')

from com_goldenthinker_trade_strategy.PabloArimaStrategy import PabloArimaStrategy
from com_goldenthinker_trade_strategy.Strategy import Strategy
from com_goldenthinker_trader_robot.Robot import Robot
from com_goldenthinker_trade_config.Config import Config
from com_goldenthinker_trade_logger.Logger import Logger

Logger.set_process_name(name='gt_buy_service')


sandbox = Config.sandbox()   

Logger.log('Initializing robot to trigger orders and signals.',telegram=True,public=True)

robot = Robot.get_instance()


strategy = PabloArimaStrategy()

strategy.subscribe(robot)
strategy.start()
