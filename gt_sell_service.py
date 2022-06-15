from com_goldenthinker_trade_datasource_network.TickerSocketMultipleSymbols import TickerSocketMultipleSymbols
from com_goldenthinker_trade_datatype.CryptoFloat import CryptoFloat
from com_goldenthinker_trade_exchange.ExchangeConfiguration import ExchangeConfiguration
from com_goldenthinker_trade_logger.Logger import Logger
from com_goldenthinker_trade_model_order.SellMarketOrder import SellMarketOrder
from com_goldenthinker_trade_config.Config import Config

from com_goldenthinker_trade_monitor.Tick import Tick
from com_goldenthinker_trade_portfolio.Portfolio import Portfolio



Logger.set_process_name('gt_sell_service')
sandbox = Config.sandbox()

monitors = {}

def update_symbols():
        with open("priority_symbols.list", 'r') as f:
                symbols_to_monitor = f.read().replace('\n','').replace(' ','').split(',')
                return symbols_to_monitor

def start_symbol_monitors(symbols_to_monitor):
        for s in symbols_to_monitor:
                monitors[s] = TickerSocketMultipleSymbols(exchange=ExchangeConfiguration.get_default_exchange(),symbols=symbols_to_monitor,callback=should_i_sell_now)
                monitors[s].start()


def should_i_sell_now(data,current_sequence):
        tick = Tick(data['data'])
        if current_sequence.should_i_sell_now():
                print('SELL NOW!')
                current_symbol = current_sequence.get_symbol()
                orders = ExchangeConfiguration.get_default_exchange().get_all_orders(current_symbol)
                order_fees = 0
                
                price_difference_highest_drop_vs_current_price_for_all_symbol_orders = [(o.get_symbol().get_current_price()-tick.get_low_price()-CryptoFloat(o.get_symbol(),order_fees)) for o in orders]
                
                # We multiply the dropping percentage for each of the orders from this symbol to mitigate the risk, as the options are 2 , rise or drop 
                # We calculate the exchanges fee for each of the orders
                
                
                percentage_change_between_highest_drop_in_tick_for_all_of_the_above = [(float(current_symbol.what_percentage_is_another_number_of_myself(order_price_difference))*2) for order_price_difference in price_difference_highest_drop_vs_current_price_for_all_symbol_orders]
                
                
                def select_existing_buy_open_orders(my_orders):
                        return [o.get_base_qty() for o in my_orders if o.get_order_type()=='MARKET' and o.get_order_side()=='BUY' and o.get_status()=='OPEN']
                
                
                buy_open_orders_for_current_symbol = select_existing_buy_open_orders(orders)
                
                
                sum_orders_for_current_symbol_base_qty =  sum([o.get_base_qty() for o in buy_open_orders_for_current_symbol])
                sum_orders_for_current_symbol_quote_amt = sum([o.get_quote_amt() for o in buy_open_orders_for_current_symbol])
                
                
                orders_for_symbol_price_change = [(current_symbol.get_current_price() - o.get_current_price() * o.get_base_qty()) for o in buy_open_orders_for_current_symbol]
                orders_for_symbol_price_change_percent = [current_symbol.what_percentage_is_another_number_of_myself(dif) for dif in orders_for_symbol_price_change ]
                
                for i in range(0..len(buy_open_orders_for_current_symbol)):
                        buy_open_orders_for_current_symbol[i].counter_order_partial(orders_for_symbol_price_change_percent[i]/2)
                
                
                
                
                
                orders_profit = sum(orders_for_symbol_price_change)
                
                probability_to_continue_losing_money
                if orders_profit < 0:
                        probability_to_continue_losing_money = orders_profit/2
                
                sell_order = SellMarketOrder(base_qty=CryptoFloat(current_sequence.get_symbol(),float_value=sum_orders_for_current_symbol_base_qty),profit=orders_profit)
                sell_order.execute()
                print('monitoring ' + str(tick) + ' sequence: ' + str(current_sequence))




portfolio = Portfolio.instance()
orders = portfolio.get_orders()
symbols_in_orders = portfolio.get_currencies_in_orders()
start_symbol_monitors(symbols_in_orders)

[(o.add_child_order(o.counter_order()),monitors[o['symbol']]) for o in orders if (o['side']=='BUY' and o['status']=='OPEN')]


once = False



    










