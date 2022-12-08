import pymongo
import psutil
import multiprocessing

from models import Poem

def make_batches(iterable, batch_size):
    result = []
    for index in range(0, len(iterable), batch_size):
        result.append(iterable[index:(index + batch_size)])
    return result

def poem_id_batches(batch_size):
    collection = pymongo.MongoClient().poetry.poems
    all_document_ids = collection.find({
        'analyzed': {'$exists': True},
        # 'rhymes': {'$exists': False},
    }).distinct('_id')
    return make_batches(all_document_ids, batch_size)

def do_batch(id_list):
    collection = pymongo.MongoClient().poetry.poems
    for _id in id_list:
        document = collection.find_one({'_id': _id})
        poem = Poem(document, collection)
        poem.set_rhymes()

def main(batch_size):
    num_cpus = psutil.cpu_count(logical=False)
    with multiprocessing.Pool(num_cpus) as pool:
        pool.map(do_batch, poem_id_batches(batch_size))

def test_single(doc_id):
    collection = pymongo.MongoClient().poetry.poems
    document = collection.find_one({'_id': doc_id})
    poem = Poem(document, collection)
    poem.set_rhymes()
        
if __name__ == '__main__':
    # main(500)
    test_single(43683)
