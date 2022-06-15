from com_goldenthinker_trade_datatype.CryptoFloat import CryptoFloat


a = CryptoFloat('eth/btc',0.000123034245)

print(a + CryptoFloat('eth/btc',0.000212345324))
