from com_goldenthinker_trade_datatype.CryptoDict import CryptoDict


# a = CryptoDict(my_dict={'hola': 1,'chau': 3 })
# b = CryptoDict(my_dict={'hola': 5,'chau': 9 })

# print(str(a+b))

# c = CryptoDict(my_dict={'hola': 1,'chau': 3 ,'rise': 4})
# d = CryptoDict(my_dict={'hola': 5,'chau': 9 ,'rise': 4 })

# print(str(c+d))

# e = CryptoDict(my_dict={'hola': 1,'chau': 3 ,'len': 4})
# f = CryptoDict(my_dict={'hola': 5,'chau': 9 ,'rise': 4 })

# print(str(e+f))

# try:

#     g = CryptoDict(my_dict={'hola': 1,'chau': 3 ,'caca': 4})
#     h = CryptoDict(my_dict={'hola': 5,'chau': 9 ,'poo': 4 })

#     print(str(g+h))
# except KeyError:
#     print("Dicts have different structure")

# try:

#     i = CryptoDict(my_dict={'hola1': 1,'chau1': 3 ,'caca': 5})
#     j = CryptoDict(my_dict={'hola1': 5,'chau1': 9 ,'caca': 5})

#     print(str(i+j))

# except KeyError:
#     print("Dicts have different structure")
    


# try:

k = CryptoDict(my_dict={'hola': 1,'chau': 3 ,'caca': {'jiji': 4, 'jojo': 2}})
l = CryptoDict(my_dict={'hola': 5,'chau': 9 ,'caca': {'jiji': 4, 'jojo': 2}})

print(str(k+l))
print(str(k-l))
print(str(k*l))
print(str(k/l))
    
# except KeyError:
#     print("Dicts have differenbt structure")
    
    
    
# m = CryptoDict(my_dict={'hola': 1,'chau': 3 ,'ris': 1})
# n = CryptoDict(my_dict={'hola': 5,'chau': 9 ,'rise': 4 })

# print(str(m+n))



# o = CryptoDict(my_dict={'hola': 'culo','chau': 3 ,'caca': {'jiji': 4, 'jojo': 2}})
# p = CryptoDict(my_dict={'hola': 'roto','chau': 9 ,'caca': {'jiji': 4, 'jojo': 2}})

# print(str(o+p))
# print(str(p+5))

#r = CryptoDict(my_dict={'hola': 'culo','chau': 3 ,'caca': {'jiji': 4, 'jojo': 2}})
#s = CryptoDict(my_dict={'hola': 'roto','chau': 9 ,'caca': {'jiji': 4, 'jojo': 2}})

#print(str(r+s))
#print(str(s+5))
#print(str(s/5))