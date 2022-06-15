from binance.spot import Spot

client = Spot()
print(client.time())

client = Spot(key='xoAWbPN2iKaPiGiQZ4TiFZ0yq2AvIdO4hBw8WrjA4AsFseXNbJ09Vd6wOAc8Siaw', secret='Ex3dbvWjN5DgpEm960nd2M2pFz40JuqQiOVmB61X23VZEifFH0fYu6CDo7yZBvra')

# Get account information
print(client.account())


#client.ticker()