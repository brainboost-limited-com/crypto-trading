from com_goldenthinker_trade_database.TinyDbConnector import TinyDbConnector

signals_from_db = TinyDbConnector.instance_for_signals().get_signals()
signals = [x for x in signals_from_db]


for s in signals:
    s.calculate_profit_and_loss()
