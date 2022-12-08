import collections
import sys

import pymongo
import pronouncing

import utils

class Poem(object):

    def __init__(self, document, collection):
        self.id = document['_id']
        self.document = document
        self.collection = collection
        
    def positions(self, attr='phones'):
        result = []
        analyzed = self.document.get('phones', [])
        for sentence_index, sentence in enumerate(analyzed):
            for word_index, word_obj in enumerate(sentence):
                r = set(pronouncing.rhyming_part(_) for _ in word_obj[attr])
                result.append(((sentence_index, word_index), r))
        return result

    def _pair_to_string(self, pair):
        return '%i,%i' % pair

    @staticmethod
    def _string_to_pair(string):
        return tuple(int(i) for i in string.split(','))
    
    def get_rhymes(self):
        rhymes = self.document.get('rhymes', {})
        result = {}
        for key, value_list in rhymes.items():
            key = self._string_to_pair(key)
            value_list = [self._string_to_pair(value) for value in value_list]
            result[key] = value_list
        return result

    def set_rhymes(self):
        self.rhymes = {}
        positions = self.positions()
        for index, (position_a, rp_a) in enumerate(positions):
            print(self.id, position_a, rp_a, index, len(positions))
            for position_b, rp_b in positions:
                if rp_a.intersection(rp_b):
                    sa, wa = position_a
                    sb, wb = position_b
                    self.document['phones'][sa][wa]['rhymes_with'].append([sb,wb])
                    self.document['phones'][sb][wb]['rhymes_with'].append([sa,wa])

        pprint.pprint(document)
        import pdb
        pdb.set_trace()
        raise 'STOP'
        self.save()
        
    def save(self):
        try:
            self.collection.update_one(
                {'_id': self.id},
                {'$set': {'rhymes': self.rhymes}},
            )
        except Exception as e:
            print(e, file=sys.stderr)

# ['beers', 'tears', 'hairs']
            
# this is a test
# better than all the rest

# 0: 0 1 2 3
# 1: 0 1 2 3 4

# (0, 0):
# (0, 1): 
