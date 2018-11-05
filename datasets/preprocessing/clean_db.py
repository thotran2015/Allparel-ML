from pymongo import MongoClient


categories = set([])

client = MongoClient('localhost', 27017)
db = client.allparel
collection = db.clothes

categories = collection.find({}, {"category": 1});

categories = [c["category"] for c in categories if ("category" in c)]
print(categories[0])

categories = list(set(categories))
for c in categories:
    print(c)
