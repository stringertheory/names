import sys
import pymongo
from models import Poem
import pprint

db = pymongo.MongoClient().poetry

document = db.poems.find_one({'_id': '10'})
poem = Poem(document, db)

pprint.pprint(poem.get_rhymes())
poem.set_rhymes()
