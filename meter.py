from __future__ import division
import numpy as np
import sys

import pymongo
import collections
from nltk.tokenize import word_tokenize
import pronouncing
import unicodedata
import pywt

def mongo_collection():
    collection = pymongo.MongoClient().poetry.poems
    return collection

CHICAGO = "2043"
TRW = "174770"
WOODS = "171621"
ROAD = "173536"
SHAKE = "174354"
STATS = "171441"

collection = mongo_collection()
for document in collection.find({"_id": STATS}, {'text': True}, limit=1):
    print >> sys.stderr, document['text']
    plain = unicodedata.normalize('NFKD', document['text'].lower()).encode('ascii','ignore').replace('-', ' ')
    stress_list = []
    for word in word_tokenize(plain):
        phones = pronouncing.phones_for_word(word)
        stresses = ''
        if phones:
            first_phone = phones[0]
            stresses = pronouncing.stresses(first_phone)
            stress_list.append(stresses)
        # print '%-20s%-20s%s' % (word, stresses, str(phones))
    signal = []
    for char in ''.join(stress_list):
        signal.append(int(char))
    c_a, c_d = pywt.dwt(signal, 'haar')
    for i, j in enumerate(signal):
        print i, j
    print ''
    # for i in c_a:
    #     print i
    # print ''
    # for i in c_d:
    #     print i
    # print ''
    ps = np.abs(np.fft.fft(signal))**2
    # for i, j in enumerate(ps):
    #     print i, j
    time_step = 1 / 10.0
    freqs = np.fft.fftfreq(len(signal), time_step)
    print >> sys.stderr, freqs
    idx = np.argsort(freqs)

    for x, y in zip(freqs[idx], ps[idx]):
        print x, y
