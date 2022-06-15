from com_goldenthinker_trade_database.MongoConnector import MongoConnector

mongo = MongoConnector.get_instance()

to_delete = [col for col in mongo.list_collection_names() if "seq_" in col]

for c in to_delete:
    print("deleting collection " + str(c))
    mongo.drop_collection(c)