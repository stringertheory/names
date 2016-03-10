import sys
import pymongo

import utils

chunk_index = int(sys.argv[1])
n_chunks = int(sys.argv[2])

limit, skip = utils.get_limit_and_skip(chunk_index, n_chunks)

db = pymongo.MongoClient().poetry

for index, document in enumerate(db.poems.find().limit(limit).skip(skip)):

    print 'process %i of %i, document %i of %i' % \
        (chunk_index + 1, n_chunks, index, limit), len(document['text'])

    for sentence in document['analyzed']:
        for word_obj in sentence:
            word = word_obj['closest']
            utils.rhymes(word)
