from __future__ import division
import numpy as np
import sys
import pprint
import string

import termcolor
import enchant
import pymongo
import collections
from nltk.tokenize import word_tokenize
import pronouncing
import unicodedata
import pywt
import unidecode

def mongo_collection():
    collection = pymongo.MongoClient().poetry.poems
    return collection

CHICAGO = "2043"
TRW = "174770"
WOODS = "171621"
ROAD = "173536"
SHAKE = "174354"
STATS = "171441"
LONG = "174987"
MILTON = "181064"
SHEL = "243466"
POEM_ID = LONG

US_DICTIONARY = enchant.request_dict("en_US")

def normalize(sentence):
    ascii_version = unidecode.unidecode(sentence.lower())
    word_list = []
    for word in ascii_version.split():
        stripped_word = word.strip(string.punctuation)
        word = stripped_word.replace("'", "")
        if '-' in word:
            for word in word.split('-'):
                word_list.append(word)
        else:
            word_list.append(word)
    plain = ' '.join(word_list)
    return plain

def stress_pattern(sentence):

    print >> sys.stderr, sentence
    
    phone_list = []
    stress_list = []
    new_sentence_list = []
    for original_word in sentence.split():

        phones = pronouncing.phones_for_word(original_word)

        word = original_word
        if not phones:

            # first try removing internal apostrophe
            word = original_word.replace("'", "")
            
            suggestions = US_DICTIONARY.suggest(word)
            print >> sys.stderr, suggestions

            for word in suggestions:

                success = True
                if ' ' in word:
                    combined = []
                    for maybe in word.split():
                        phones = pronouncing.phones_for_word(maybe)
                        if not phones:
                            success = False
                            break
                        else:
                            combined.append(phones[0])
                    
                phones = pronouncing.phones_for_word(word)
                if phones:
                    print >> sys.stderr, 'corrected %s to %s' % \
                        (original_word, word)
                    break

            if word == original_word:
                
                suggestions = US_DICTIONARY.suggest(original_word)
                print >> sys.stderr, suggestions

                for word in suggestions:
                    phones = pronouncing.phones_for_word(word)
                    if phones:
                        print >> sys.stderr, 'corrected %s to %s' % \
                            (original_word, word)
                        break
                
        new_sentence_list.append(word)
            
        stresses = ''
        if phones:
            first_phone = phones[0]
            phone_list.append(first_phone)
            stresses = pronouncing.stresses(first_phone)
            stress_list.append(stresses)
    
    signal = []
    for char in ''.join(stress_list):
        signal.append(int(char) % 2)

    print >> sys.stderr, ' '.join(new_sentence_list)
    print >> sys.stderr, signal, len(signal)
    print >> sys.stderr, ''
        
    return signal

collection = mongo_collection()
for document in collection.find({"_id": POEM_ID}, limit=1):

    print document
    
    pprint.pprint(document['text'], sys.stderr)

    normalized = [normalize(sentence) for sentence in document['text']]

    stresses = [stress_pattern(sentence) for sentence in normalized]

    for signal in stresses:
        block_list = []
        for i in signal:
            if i:
                block_list.append(termcolor.colored(' ', 'green', 'on_blue'))
            else:
                block_list.append(termcolor.colored(' ', 'green', 'on_yellow'))
                                
        print ''.join(block_list)
        
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
