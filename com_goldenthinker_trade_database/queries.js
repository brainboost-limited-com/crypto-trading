/* mongo-formula */ ``
var oldest = new Date(new Date() - new Date(15 * 60000));
print(oldest);

var collections = db.getCollectionNames();
print(collections);

collections.forEach(function(item){
    db.getCollection(item).find({timestamp: { // 18 minutes ago (from now)
        $gt: new Date(ISODate().getTime() - 1000 * 60 * 18);
    }},fuction(err,docs){
        print(docs);
    });

});