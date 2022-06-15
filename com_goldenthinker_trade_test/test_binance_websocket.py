import time

from binance import ThreadedWebsocketManager

api_key = 'xoAWbPN2iKaPiGiQZ4TiFZ0yq2AvIdO4hBw8WrjA4AsFseXNbJ09Vd6wOAc8Siaw'
api_secret = 'Ex3dbvWjN5DgpEm960nd2M2pFz40JuqQiOVmB61X23VZEifFH0fYu6CDo7yZBvra'

def main():

    symbol = 'BNBBTC'

    twm = ThreadedWebsocketManager(api_key=api_key, api_secret=api_secret)
    # start is required to initialise its internal loop
    twm.start()

    def handle_socket_message(msg):
       # print(f"message type: {msg['e']}")
        print(msg)

    #twm.start_kline_socket(callback=handle_socket_message, symbol=symbol)

    # multiple sockets can be started
    twm.start_depth_socket(callback=handle_socket_message, symbol=symbol)

    # or a multiplex socket can be started like this
    # see Binance docs for stream names
    #streams = [ 'bnbbtc@bookTicker']
    #twm.start_multiplex_socket(callback=handle_socket_message, streams=streams)

    twm.join()


if __name__ == "__main__":
   main()