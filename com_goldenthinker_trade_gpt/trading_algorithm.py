import ta
import numpy as np

class TradingAlgorithm:
    def generate_signals(self, prices):
        closes = np.array(list(prices.values()))
        sma20 = ta.trend.sma_indicator(closes, window=20)
        sma50 = ta.trend.sma_indicator(closes, window=50)
        ema9 = ta.trend.ema_indicator(closes, window=9)
        
        signals = {}
        for symbol, price in prices.items():
            if ema9[-1] > sma20[-1] and ema9[-1] > sma50[-1]:
                signals[symbol] = 'BUY'
            elif ema9[-1] < sma20[-1] and ema9[-1] < sma50[-1]:
                signals[symbol] = 'SELL'
        return signals
    
    def generate_orders(self, signals, prices):
        orders = []
        for symbol, signal in signals.items():
            if signal == 'BUY':
                orders.append({
                    'symbol': symbol,
                    'side': 'BUY',
                    'type': 'LIMIT',
                    'quantity': 0.001,
                    'price': prices[symbol]
                })
            elif signal == 'SELL':
                orders.append({
                    'symbol': symbol,
                    'side': 'SELL',
                    'type': 'LIMIT',
                    'quantity': 0.001,
                    'price': prices[symbol]
                })
        return orders
