import itertools
import sys

import functools
import pronouncing
import editdistance
import g2p_en

g2p_phones = g2p_en.G2p()
pronouncing.init_cmu()

def unpack(word_list):
    return list(itertools.product(*word_list))

@functools.lru_cache()
def phones_for_closest_match(word):
    """Brute force. Look for lowest distance between all words that are in
    the CMU dictionary.

    """
    by_distance = []
    for possibility, phones in pronouncing.pronunciations:

        # levenstein
        distance = editdistance.eval(possibility, word)

        # give a bonus for same first letter / last letter
        if possibility.startswith(word[0]):
            distance -= 1
        if possibility.endswith(word[-1]):
            distance -= 1 

        # break ties with difference in length
        character_difference = abs(len(possibility) - len(word))
        by_distance.append((distance, character_difference, possibility))

    # find the lowest (final tie breaker is alphabetical, oh well)
    d_edit, d_length, suggestion = min(by_distance)

    phones = pronouncing.phones_for_word(suggestion)
    
    # return the phones for the suggestion
    return phones

@functools.lru_cache()
def phones_for_word(word):
    """Look up a word in the CMU dictionary for it's phones. If it's not
    in there, first deal with hyphens and then use an approximate
    match as a fallback.

    """
    # return a blank phone string for a blank word
    if not word:
        return ['']

    # try to look up in dictionary
    phones = pronouncing.phones_for_word(word)
    if phones:
        return phones

    # for hyphenated words, look up each word independently and then
    # join back up
    if "-" in word:
        phones = []
        for group in unpack([phones_for_word(_) for _ in word.split('-')]):
            phones.append(' '.join(_ for _ in group if _))
        return list(set(phones))

    # fall back to g2p
    try:
        result = [' '.join(g2p_phones(word))]
    except:
        pass
    else:
        return result

    # final fallback is finding nearest word
    return phones_for_closest_match(word)

if __name__ == '__main__':
    
    words = [
        "pirmit",
        "improbable",
        "tears",
        "mountain-side",
        "mountain-tears",
        "permit-tears",
        "nakedness",
        "untrimm'd",
        "untrimmed",
        "factorize",
        "duncan-phyfe",
        "duncan-fife",
        "fuck-the-work-week",
        "meat--attends",
        "san'angelo",
        'hiving-out--and',
    ]

    for word in words:
        pho1 = g2p_phones(word)
        pho2 = phones_for_word(word)
        print('word\t', word)
        print('g2p\t', ' '.join(pho1))
        print('all\t', pho2)
        for phones in pho2:
            print(phones, '|', pronouncing.rhyming_part(phones))
        print()

