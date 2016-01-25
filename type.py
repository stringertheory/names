import pymongo
import collections
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
stop = set(stopwords.words('english'))

def mongo_collection():
    collection = pymongo.MongoClient().poetry.poems
    return collection

counter = collections.Counter()
collection = mongo_collection()
for index, i in enumerate(collection.find({'POETIC TERMS': 'Sonnet'})):
    print index, len(i['text']), i['_id']


