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
for i in collection.find(None, {'text': True}):
    for word in word_tokenize(i['text']):
        counter[word.lower()] += 1

rank = 1
for index, (word, count) in enumerate(counter.most_common(), 1):
    if word in stop:
        msg = '%i\t%s\t%i\t%s' % (index, '', count, word)
    else:
        msg = '%i\t%i\t%i\t%s' % (index, rank, count, word)
        rank += 1
    print(msg.encode('utf8'))

