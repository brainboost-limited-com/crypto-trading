python
from binance_p2p import BinanceP2P

def main(api_key, api_secret):
    binance_p2p = BinanceP2P(api_key, api_secret)
    currencies = binance_p2p.get_available_currencies()
    payment_methods = binance_p2p.get_available_payment_methods()
    print("Available currencies:", currencies)
    print("Available payment methods:", payment_methods)

if __name__ == "__main__":
    api_key = "YOUR_API_KEY"
    api_secret = "YOUR_API_SECRET"
    main(api_key, api_secret)