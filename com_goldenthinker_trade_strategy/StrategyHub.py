

from com_goldenthinker_trade_strategy.PabloArimaStrategy import PabloArimaStrategy


class StrategyHub:
    
    
    # Evaluate what strategy or combination of strategies to use
    
    @classmethod
    def strategy_to_use(self):
        return PabloArimaStrategy(robot=None,data=None)