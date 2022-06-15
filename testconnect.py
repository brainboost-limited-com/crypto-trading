import pymongo
conn = pymongo.MongoClient('mongodb://Administrator:Papapa123.@localhost:27017/')
db = conn['goldenthinker']
coll = db['collection']