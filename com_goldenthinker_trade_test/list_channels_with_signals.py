from tinydb.database import TinyDB
from tinydb import Query



db = TinyDB('storage/signals.json')
q = Query()

texts = [q.get('channel') for q in db.search(q.channel.exists())]

for e in set(texts):
    print(str(e))