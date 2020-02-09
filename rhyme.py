import sys
import pymongo

from models import Poem

chunk_index = int(sys.argv[1])
n_chunks = int(sys.argv[2])

limit, skip = utils.get_limit_and_skip(chunk_index, n_chunks)

db = pymongo.MongoClient().poetry

for index, document in enumerate(db.poems.find().limit(limit).skip(skip)):
    
    print('process %i of %i, document %i of %i (_id: %s)' % \
        (chunk_index + 1, n_chunks, index, limit, document['_id']))

    poem = Poem(document, db)
    poem.set_rhymes()


    
