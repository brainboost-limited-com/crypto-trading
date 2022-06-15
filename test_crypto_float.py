from com_goldenthinker_trade_datatype.CryptoFloat import CryptoFloat
from com_goldenthinker_trade_model.Symbol import Symbol
from com_goldenthinker_trade_database.MongoConnector import MongoConnector

a = CryptoFloat(Symbol('ETHBTC'),0.00122343)
MongoConnector.get_instance().insert_test(number=dict(a.get_value()))


print(dict(a))