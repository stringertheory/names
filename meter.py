from __future__ import division
import numpy as np
import sys
import pprint
import string
import collections
import functools32
import termcolor
import enchant
import pymongo
import collections
from nltk.tokenize import word_tokenize
import pronouncing
import unicodedata
import pywt
import unidecode

import distance
import poem_ids

def mongo_collection():
    collection = pymongo.MongoClient().poetry.poems
    return collection

NO_PHONES = open('NO_PHONES.txt', 'a')
ACCEPTED_SUGGESTIONS = open('ACCEPTED_SUGGESTIONS.txt', 'a')
US_DICTIONARY = enchant.request_dict("en_US")


def word_tokenize(sentence):
    ascii_version = unidecode.unidecode(sentence.lower())
    word_list = []
    for word in ascii_version.split():
        stripped = word.strip(string.punctuation).strip()
        if stripped:
            word_list.append(stripped)
    return word_list

def phones_for_suggestion(with_spaces):

    success = True
    result = []
    for part in with_spaces.split():
        phones = pronouncing.phones_for_word(part)
        if phones:
            result.append(phones[0])
        else:
            success = False
            break
        
    if success:
        phones = [' '.join(result)]
    else:
        phones = []

    return phones

def phones_for_sentence(word_list):
    
    approximate_words = []
    phones_list = []
    for word in word_list:

        replacement, phones = distance.phones_for_word(word)

        approximate_words.append(replacement)

        # for now, just pick first alternative from list
        phones_list.append(phones[0])

    return approximate_words, phones_list
        
def stress_pattern(phones):
    return pronouncing.stresses(''.join(p for p in phones))

IGNORE = set([
    '172777', # beowulf
])

collection = mongo_collection()
# for document in collection.find({"_id": poem_ids.POEM_ID}, limit=1):
for document in collection.find(None, limit=1):

    print >> sys.stderr, document['_id']

    normalized = [word_tokenize(sentence) for sentence in document['text']]
    approximate = []
    phones = []
    for sentence in normalized:
        a, p = phones_for_sentence(sentence)
        approximate.append(a)
        phones.append(p)
    stresses = [stress_pattern(sentence) for sentence in phones]
    print len(normalized), len(approximate), len(phones), len(stresses)
    analyzed = []
    for n, a, p in zip(normalized, approximate, phones):
        sentence = []
        for n_, a_, p_ in zip(n, a, p):
            word = {
                'ascii': n_,
                'closest': a_,
                'phones': p_,
            }
            sentence.append(word)
        analyzed.append(sentence)
    
    document['analyzed'] = analyzed
    document['stresses'] = stresses
    collection.save(document)
    
    row_list = []
    for signal in stresses:
        terminal = []
        block_list = []
        for i in signal:
            if int(i):
                block_list.append('<div class="diagram stressed"></div>')
                terminal.append(termcolor.colored('  ', 'green', 'on_blue'))
            else:
                terminal.append(termcolor.colored('  ', 'green', 'on_yellow'))
                block_list.append('<div class="diagram unstressed"></div>')

        row = '<div class="diagram sentence">%s</div>' % ''.join(block_list)
        row_list.append(row)
        print >> sys.stderr, ''.join(terminal)

    diagram = '<div class="diagram container">%s</div>' % ''.join(row_list)

    with open('formatted/%s.html' % document['_id'], 'w') as outfile:
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

    # c_a, c_d = pywt.dwt(signal, 'haar')
    #     for i, j in enumerate(signal):
    #         print i, j
    #     print ''
    # # for i in c_a:
    # #     print i
    # # print ''
    # # for i in c_d:
    # #     print i
    # # print ''
    # ps = np.abs(np.fft.fft(signal))**2
    # # for i, j in enumerate(ps):
    # #     print i, j
    # time_step = 1
    # freqs = np.fft.fftfreq(len(signal), time_step)
    # print >> sys.stderr, freqs
    # idx = np.argsort(freqs)

    # for x, y in zip(freqs[idx], ps[idx]):
    #     print x, y

