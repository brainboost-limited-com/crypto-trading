

from com_goldenthinker_trade_model.Symbol import Symbol
from com_goldenthinker_trade_model_order.BuyMarketOrder import BuyOrder

s = Symbol('btc/usdt')
a = s.min_quantity_i_can_buy()
b = s.max_quantity_i_can_buy()
c = s.min_amount_i_can_spend()
d = s.max_amount_i_can_spend()
e = s.percent_to_amount(percent_to_amount_according_balance=5)
#f = s.closest_possible_amount_to_quantity(0.09890987)

#orders = s.get_all_orders()

#o = BuyOrder(amount=CryptoFloat('quick/usdt',quote_amt=10.10))

#o = SellMarketOrder(amount=CryptoFloat('bnb/usdt',quote_amt=10.10))
#o.execute()

o1 = BuyOrder(symbol=Symbol('BTCUSDT'),ptg=20)
o1.execute()