import sys
import string
import termcolor
import pymongo
import pronouncing
import unidecode
import itertools
import collections

import poem_ids
import distance
import utils

def mongo_collection():
    collection = pymongo.MongoClient().poetry.poems
    return collection


def make_row(sentence, rhyme_words):
    block_list = []
    for word_obj in sentence:
        if word_obj['closest'] in rhyme_words:
            color_index = 1
        else:
            color_index = 0
        block = '<span class="diagram word color-%i">%s</span>' % \
            (color_index, word_obj['closest'])
        block_list.append(block)
    row = '<div class="diagram sentence">%s</div>' % ''.join(block_list)
    return row

collection = mongo_collection()
for document in collection.find({"_id": poem_ids.STATS}).limit(1):

    print >> sys.stderr, document['_id']
    
    n_sentences = len(document['analyzed'])
    row_list = []
    for line_number, sentence in enumerate(document['analyzed'][1:-1], 1):
        line_number_before = line_number - 1
        sentence_before = document['analyzed'][line_number_before]
        line_number_after = line_number + 1
        sentence_after = document['analyzed'][line_number_after]

        rhyme_words = set()
        word_list = list(set(w['closest'] for w in sentence_before + sentence + sentence_after))
        for index, word_a in enumerate(word_list):
            rhymes_a = set(utils.rhymes(word_a))
            for word_b in word_list[(index + 1):]:
                if word_b in rhymes_a:
                    rhyme_words.add(word_a)
                    rhyme_words.add(word_b)

        if line_number_before == 0:
            row_list.append(make_row(sentence_before, rhyme_words))
        row_list.append(make_row(sentence, rhyme_words))
        if line_number_after == (n_sentences - 1):
            row_list.append(make_row(sentence_after, rhyme_words))

            
    diagram = '<div class="diagram container">%s</div>' % ''.join(row_list)

    with open('rhymes/%s.html' % document['_id'], 'w') as outfile:
        outfile.write('<html>')
        outfile.write('<head>')
        outfile.write('<link rel="stylesheet" type="text/css" href="diagram.css">')
        outfile.write('</head>')
        outfile.write('<body>')
        outfile.write(document['html'].encode('utf8'))
        outfile.write('\n')
        outfile.write(diagram)
        outfile.write('\n')
        outfile.write('</body>')
        outfile.write('</html>')

