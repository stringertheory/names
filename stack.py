import sys
import pymongo
import collections

import poem_ids

def mongo_collection():
    collection = pymongo.MongoClient().poetry.poems
    return collection

collection = mongo_collection()
query = {
    "stresses": {
        "$exists": True,
    },
}
num = collections.Counter()
den = collections.Counter()
for document in collection.find(query, no_cursor_timeout=True):
    for signal in document['stresses']:
        for x, z in enumerate(signal, 1):
            den[x] += 1
            if int(z):
                num[x] += 1
                
for i, d in sorted(den.items()):
    print(i, num[i] / float(d))

print('')
