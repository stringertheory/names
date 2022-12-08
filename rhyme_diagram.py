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


def make_row(sentence, rhyme_index):
    block_list = []
    for word_index, word_obj in enumerate(sentence):
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
for document in collection.find({"_id": 55343}).limit(1):

    print(document['_id'], file=sys.stderr)
    for index, line in enumerate(document['analyzed']):
        print(index, ' '.join(w['closest'] for w in line))

    colors = [1, 2, 3]
    color_index = 0
    rhyme_index = {}
    for key, r_list in document['rhymes'].items():
        sa, wa = tuple(int(_) for _ in key.split(','))
        color = colors[color_index % len(colors)]
        document['analyzed'][sa][wa]['color'] = color
        print(document['analyzed'][sa][wa]['closest'], color, end=': ')
        for r in r_list:
            sb, wb = tuple(int(_) for _ in r.split(','))
            word = document['analyzed'][sb][wb]
            word['color'] = color
            print(word['closest'], end=', ')
        print()
            
        color_index += 1

    row_list = []
    for sentence_index, sentence in enumerate(document['analyzed']):
        span_list = []
        for word_index, word in enumerate(sentence):
            color = word.get('color', 0)
            closest = word['closest']
            span = f'<span class="diagram word color-{color}">{closest}</span>'
            span_list.append(span)
        row = '<div class="diagram sentence">{}</div>'.format(''.join(span_list))
        row_list.append(row)

    diagram = '<div class="diagram container">{}</div>'.format(''.join(row_list))

    filename = f'rhymes/{document["_id"]}.html'
    print(filename)
    with open(filename, 'w') as outfile:
        outfile.write('<html>')
        outfile.write('<head>')
        outfile.write('<link rel="stylesheet" type="text/css" href="diagram.css">')
        outfile.write('</head>')
        outfile.write('<body>')
        outfile.write(document['html'])
        outfile.write('\n')
        outfile.write(diagram)
        outfile.write('\n')
        outfile.write('</body>')
        outfile.write('</html>')

