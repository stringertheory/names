import pprint
import sys
import string
import termcolor
import pymongo
import pronouncing
import unidecode
from Bio import pairwise2
    
import distance

MAX_RHYME_SEARCH_LINES = 50

import unicodedata
import sys

UNICODE_PUNCTUATION = dict.fromkeys(
    i for i in range(sys.maxunicode)
    if unicodedata.category(chr(i)).startswith('P')
)

def remove_punctuation(text):
    return text.translate(UNICODE_PUNCTUATION)

def mongo_collection():
    collection = pymongo.MongoClient().poetry.poems
    return collection

def aligned(original, normalized):
    if len(original) == len(normalized):
        return original, normalized
    else:
        alignments = pairwise2.align.globalxx(original, normalized, gap_char=[''], match_fn=lambda x,y: bool(x.lower() == y.lower()))
        try:
            best = alignments[0]
        except Exception:
            return normalized, normalized
        else:
            a, b, score, start, end = best
            a = [_ for _ in a if _]
            b = [_ for _ in b if _]
            if len(a) == len(b):
                return a, b
            else:
                return normalized, normalized

def word_tokenize(sentence):
    original = [remove_punctuation(_).strip() for _ in sentence.split()]
    ascii_version = unidecode.unidecode(sentence.lower())
    word_list = []
    for word in ascii_version.split():
        stripped = word.strip(string.punctuation).strip()
        if stripped:
            word_list.append(stripped)
    return aligned(original, word_list)
        
def stress_pattern(phones):
    return pronouncing.stresses(''.join(p for p in phones))

#, {'_id': 50114} <-- beowulf
collection = mongo_collection()
for index, document in enumerate(collection.find(no_cursor_timeout=True).sort("_id", pymongo.DESCENDING).batch_size(20), 1):
    
    if 'analyzed' in document or not 'lines' in document:
        print(index, 'skipping %s' % document['_id'], file=sys.stderr)
        continue
    else:
        print(index, 'analyzing %s' % document['_id'], file=sys.stderr)

    normalized_sentences = []
    original_sentences = []
    for sentence in document['lines']:
        original, asciified = word_tokenize(sentence)
        normalized_sentences.append(asciified)
        original_sentences.append(original)
    
    all_phones = []
    for asciified in normalized_sentences:
        sentence_phones = [distance.phones_for_word(_) for _ in asciified]
        all_phones.append(sentence_phones)
            
    analyzed = []
    for s_i, (n, o, p) in enumerate(zip(normalized_sentences, original_sentences, all_phones)):
        sentence = []
        for w_i, (n_, o_, p_) in enumerate(zip(n, o, p)):
            word = {
                'word': o_,
                'ascii': n_,
                'position': (s_i, w_i),
                'phones': p_,
                'rhymes_with': set(),
            }
            sentence.append(word)
        analyzed.append(sentence)
        
    positions = []
    for sentence_index, sentence in enumerate(analyzed):
        for word_index, word_obj in enumerate(sentence):
            r = set(pronouncing.rhyming_part(_) for _ in word_obj['phones'])
            positions.append(((sentence_index, word_index), r))

    for (sa, wa), rp_a in positions:
        for (sb, wb), rp_b in positions:
            if abs(sa - sb) <= MAX_RHYME_SEARCH_LINES:
                if (sa, wa) != (sb, wb) and rp_a.intersection(rp_b):
                    analyzed[sa][wa]['rhymes_with'].add((sb, wb))
                    analyzed[sb][wb]['rhymes_with'].add((sa, wa))

    for sentence in analyzed:
        for word in sentence:
            word['rhymes_with'] = list(sorted(word['rhymes_with']))

    try:
        collection.update_one(
            {'_id': document.get('_id')},
            {'$set': {'analyzed': analyzed}},
        )
    except Exception as e:
        print(index, e)
        continue
    
    
    # print(index, 'inserted', document['_id'])
    
    # row_list = []
    # for signal, line in zip(stresses, document['lines']):
    #     terminal = []
    #     block_list = []
    #     for i in signal:
    #         if int(i):
    #             block_list.append('<div class="diagram stressed"></div>')
    #             terminal.append(termcolor.colored('  ', 'green', 'on_blue'))
    #         else:
    #             terminal.append(termcolor.colored('  ', 'green', 'on_yellow'))
    #             block_list.append('<div class="diagram unstressed"></div>')

    #     row = '<div class="diagram sentence">%s</div>' % ''.join(block_list)
    #     row_list.append(row)
    #     print(''.join(terminal), file=sys.stderr)

    # diagram = '<div class="diagram container">%s</div>' % ''.join(row_list)

    # with open('formatted/%s.html' % document['_id'], 'w') as outfile:
    #     outfile.write('<html>')
    #     outfile.write('<head>')
    #     outfile.write('<link rel="stylesheet" type="text/css" href="diagram.css">')
    #     outfile.write('</head>')
    #     outfile.write('<body>')
    #     outfile.write(document['html'])
    #     outfile.write('\n')
    #     outfile.write(diagram)
    #     outfile.write('\n')
    #     outfile.write('</body>')
    #     outfile.write('</html>')

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

