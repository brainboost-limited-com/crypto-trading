from com_goldenthinker_trade_database.MongoConnector import MongoConnector

class MongoImporter:
    
    
    
    def __init__(self,connection_str):
        self.connection_str = connection_str
        self.mongo = MongoConnector.get_instance()
        
        
    def import_all_collections_into_server(self,connection_str):
        collection_names = self.mongo.list_collection_names()
        for c in collection_names:
            mongo_import_command = "mongoimport --uri " + connection_str + " --drop --collection " + str(c) + " --file " + "/ec2/mongo_backup/" + str(c) + ".bson"
            
            
        
        
        
connection = "mongoimport --uri mongodb+srv://goldenthinker:justice@goldenthinker.ooed3.mongodb.net/goldenthinker?retryWrites=true&w=majority --drop --collection collectionName --file localFileLocation"

importer = MongoImporter(connection)
importer.import_all_collections_into_server("mongodb+srv://goldenthinker:justice@goldenthinker.ooed3.mongodb.net/goldenthinker?retryWrites=true&w=majority")