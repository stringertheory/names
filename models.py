import sys

import pymongo

import utils

class Poem(object):

    def __init__(self, document, collection):
        self.id = document['_id']
        self.document = document
        self.collection = collection
        
    def positions(self, attr='closest'):
        result = []
        analyzed = self.document.get('analyzed', [])
        for sentence_index, sentence in enumerate(analyzed):
            for word_index, word_obj in enumerate(sentence):
                result.append(((sentence_index, word_index), word_obj[attr]))
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
        for index, (position_a, word_a) in enumerate(positions):
            rhymes_a = utils.rhymes(word_a)
            print(self.id, position_a, word_a, index, len(positions))
            for position_b, word_b in positions[(index+1):]:
                if word_b in rhymes_a:
                    key = '%i,%i' % position_a
                    value = '%i,%i' % position_b
                    try:
                        self.rhymes[key].append(value)
                    except KeyError:
                        self.rhymes[key] = [value]

        self.document['rhymes'] = self.rhymes
        self.save()
        
    def save(self):
        try:
            self.collection.update_one(
                {'_id': self.id},
                {'$set': {'rhymes': self.rhymes}},
            )
        except Exception as e:
            print(e, file=sys.stderr)
            
