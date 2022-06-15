from kraken_wsclient_py import kraken_wsclient_py as client

def my_handler(message):
    # Here you can do stuff with the messages
    print(message)

my_client = client.WssClient()
my_client.start()

# Sample public-data subscription:

my_client.subscribe_public(
    subscription = {
        'name': 'trade'
    },
    pair = ['XBT/USD', 'XRP/USD'],
    callback = my_handler
)

# Sample private-data subscription:

my_client.subscribe_private(
    subscription = {
        'name': 'openOrders',
        'token': '__WS_TOKEN_HERE__'
    },
    callback = my_handler
)

# Sample order-entry call:

my_client.request(
    request = {
        'token': '__WS_TOKEN_HERE__',
        'event': 'addOrder',
        'type': 'buy',
        'ordertype': 'limit',
        'pair': 'XBT/USD',
        'price': '9000',
        'volume': '0.01',
        'userref': '666'
    },
    callback = my_handler
)