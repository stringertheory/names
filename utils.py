
import functools
import pymongo

db = pymongo.MongoClient().poetry

@functools.lru_cache(maxsize=2**20)
def rhymes(word):
    
    query_result = db.rhymes.find_one({'word': word})

    if query_result is None:
        result = pronouncing.rhymes(word)
        db.rhymes.save({'word': word, 'rhymes': list(result)})

    else:
        result = set(query_result['rhymes'])

    return result

def get_limit_and_skip(index, n_split):

    index = int(index)
    n_split = int(n_split)
    
    total = int(db.poems.count())

    per_split = total / n_split
    extra = total % n_split
    sizes = [per_split] * n_split
    for i in range(extra):
        sizes[i] += 1
    result = []
    start_index = 0
    cumulative = 0
    for size in sizes:
        result.append((size, start_index))
        start_index += size
    return result[index]
