from binance.client import Client
import concurrent.futures

class BinanceClient:
    def __init__(self, api_key, api_secret):
        self.client = Client(api_key, api_secret)
    
    def get_symbol_prices(self, symbols):
        with concurrent.futures.ThreadPoolExecutor() as executor:
            futures = {executor.submit(self.client.get_symbol_ticker, symbol): symbol for symbol in symbols}
            prices = {}
            for future in concurrent.futures.as_completed(futures):
                symbol = futures[future]
                try:
                    prices[symbol] = float(future.result()['price'])
                except Exception as e:
                    print(f'Exception while getting {symbol} price: {e}')
        return prices
    
    def execute_orders(self, orders):
        for order in orders:
            try:
                response = self.client.create_order(
                    symbol=order['symbol'],
                    side=order['side'],
                    type=order['type'],
                    quantity=order['quantity'],
                    price=order['price']
                )
                print(f"Executed order: {response}")
            except Exception as e:
                print(f"Error executing order: {e}")
