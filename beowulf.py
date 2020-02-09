IGNORE = set([
    '172777', # beowulf
])
import sys
import pymongo
import collections

import poem_ids

def mongo_collection():
    collection = pymongo.MongoClient().poetry.poems
    return collection

collection = mongo_collection()
query = {
    "_id": "172777",
}
for document in collection.find(query, no_cursor_timeout=True):
    for sentence in document['analyzed']:
        for word in sentence:
            print(word['closest'], end=' ')
        print('')
