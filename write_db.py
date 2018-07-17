from pymongo import MongoClient


client = MongoClient('localhost', 27017)

db = client.allparel

collection = db.clothes

item = {
         'filename': 'filename', 
         'image_filename': 'image_filename',
         'url': 'url',
         'description': 'description',
         'allparel_labels': ['l1', 'l2']
        }

#post_id = collection.insert_one(item).inserted_id
#print(post_id)
print(collection.find_one({'filename':'filename'}))
collection.update({'filename':'filename'}, { '$set': {'description':'NEW'}})
print(collection.find_one({'filename':'filename'}))
