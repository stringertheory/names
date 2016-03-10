import sys
import string
import termcolor
import pymongo
import pronouncing
import unidecode

import distance

# a decorator that caches functions but stores results with a db backend would be nice.

def mongo_collection():
    collection = pymongo.MongoClient().poetry.poems
    return collection

def word_tokenize(sentence):
    ascii_version = unidecode.unidecode(sentence.lower())
    word_list = []
    for word in ascii_version.split():
        stripped = word.strip(string.punctuation).strip()
        if stripped:
            word_list.append(stripped)
    return word_list

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

collection = mongo_collection()
for document in collection.find(no_cursor_timeout=True).sort("_id", pymongo.DESCENDING).batch_size(5):
    
    if 'analyzed' in document:
        print >> sys.stderr, 'skipping %s' % document['_id']
        continue
    else:
        print >> sys.stderr, 'analyzing %s' % document['_id']
    
    normalized = [word_tokenize(sentence) for sentence in document['text']]

    approximate = []
    phones = []
    for sentence in normalized:
        a, p = phones_for_sentence(sentence)
        approximate.append(a)
        phones.append(p)

    stresses = [stress_pattern(sentence) for sentence in phones]

    # zip up for easier storage
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

