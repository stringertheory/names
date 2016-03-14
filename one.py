import sys
import pymongo
from models import Poem
import pprint
import utils
import pronouncing

print pronouncing.rhymes('a')
print pronouncing.rhymes('the')
raise 'STOp'

db = pymongo.MongoClient().poetry

document = db.poems.find_one({'_id': '10'})
poem = Poem(document, db)

pprint.pprint(poem.get_rhymes())
poem.set_rhymes()
