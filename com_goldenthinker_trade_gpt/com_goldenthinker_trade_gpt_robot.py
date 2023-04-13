import websocket
import json
import talib
import numpy as np
from binance.client import Client
from binance.enums import *
from dotenv import load_dotenv
import os
import time

# Load the environment variables
load_dotenv()

# Define the Binance API key and secret
binance_api_key = os.getenv('BINANCE_API_KEY')
binance_api_secret = os.getenv('BINANCE_API_SECRET')

# Define the client
client = Client(binance_api_key, binance_api_secret)

# Define the symbols to monitor
symbols = [symbol['symbol'] for symbol in client.get_exchange_info()['symbols']]

# Define the technical indicators
def rsi_indicator(data, period):
    return talib.RSI(data, timeperiod=period)[-1]

def ema_indicator(data, period):
    return talib.EMA(data, timeperiod=period)[-1]

def macd_indicator(data, fast_period, slow_period, signal_period):
    macd, signal, _ = talib.MACD(data, fastperiod=fast_period, slowperiod=slow_period, signalperiod=signal_period)
    return macd[-1] - signal[-1]

# Define the signal generation function
def generate_signal(symbol, interval):
    # Define the variables
    candlesticks = []
    rsi_period = 14
    ema_period = 50
    macd_fast_period = 12
    macd_slow_period = 26
    macd_signal_period = 9
    amount_precision = client.get_symbol_info(symbol)['quoteAssetPrecision']
    amount_min = float(client.get_symbol_info(symbol)['filters'][2]['minQty'])

    # Define the WebSocket on_open callback function
    def on_open(ws):
        print('WebSocket connection opened')

    # Define the WebSocket on_close callback function
    def on_close(ws):
        print('WebSocket connection closed')

    # Define the WebSocket on_message callback function
    def on_message(ws, message):
        # Parse the message as JSON
        json_message = json.loads(message)

        # Check if the message is a candlestick
        if json_message['e'] == 'kline':
            # Parse the candlestick data
            candlestick = json_message['k']
            candlestick_close = float(candlestick['c'])

            # Append the candlestick data to the list
            candlesticks.append(candlestick_close)

            # Check if we have enough data to calculate the indicators
            if len(candlesticks) >= max(rsi_period, ema_period, macd_slow_period + macd_signal_period):
                # Convert the candlesticks data to a NumPy array
                candlesticks_np = np.array(candlesticks)

                # Calculate the indicators
                rsi = rsi_indicator(candlesticks_np, rsi_period)
                ema = ema_indicator(candlesticks_np, ema_period)
                macd = macd_indicator(candlesticks_np, macd_fast_period, macd_slow_period, macd_signal_period)

                # Generate the signal
                if rsi < 30 and candlestick_close < ema and macd > 0:
                    # Buy signal
                    order = client.order_market_buy(symbol=symbol, quantity=amount_min)
                    print(f'Buy signal generated for {symbol} on interval {interval}: {order}')
                elif rsi > 70 and candlestick_close > ema and macd
            < 0:
                # Sell signal
                quantity = client.get_asset_balance(asset=symbol[:-3])['free']
                order = client.order_market_sell(symbol=symbol, quantity=quantity)
                print(f'Sell signal generated for {symbol} on interval {interval}: {order}')

# Define the WebSocket error callback function
def on_error(ws, error):
    print(error)

# Define the WebSocket URL
ws_url = f'wss://stream.binance.com:9443/ws/{symbol.lower()}@kline_{interval}'

# Create the WebSocket
ws = websocket.WebSocketApp(ws_url, on_open=on_open, on_close=on_close, on_message=on_message, on_error=on_error)

# Run the WebSocket
ws.run_forever()





def main():
    # Define the WebSocket URL
    socket_url = 'wss://stream.binance.com:9443/ws'

    # Define the WebSocket streams
    kline_streams = [f'{symbol.lower()}@kline_1m' for symbol in symbols]

    # Define the WebSocket on_error callback function
    def on_error(ws, error):
        print(error)

    # Define the WebSocket on_open callback function
    def on_open(ws):
        # Subscribe to the Kline streams
        for stream in kline_streams:
            ws.send(json.dumps({'method': 'SUBSCRIBE', 'params': [stream], 'id': 1}))

    # Define the WebSocket on_close callback function
    def on_close(ws):
        print('WebSocket connection closed')

    # Define the WebSocket on_message callback function
    def on_message(ws, message):
        pass  # The on_message callback function has been defined earlier

    # Define the WebSocket app
    ws_app = websocket.WebSocketApp(socket_url,
                                    on_error=on_error,
                                    on_open=on_open,
                                    on_close=on_close,
                                    on_message=on_message)

    # Start the WebSocket app
    ws_app.run_forever()
