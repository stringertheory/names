import sys

import functools
import pronouncing
import editdistance

pronouncing.init_cmu()

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

    # return the suggestion and the phones for the suggestion
    return suggestion, phones

@functools.lru_cache()
def phones_for_word(word):
    """Look up a word in the CMU dictionary for it's phones. If it's not
    in there, first deal with hyphens and then use an approximate
    match as a fallback.

    """
    # return a blank phone string for a blank word
    if not word:
        return word, ['']

    # try to look up in dictionary
    phones = pronouncing.phones_for_word(word)
    if phones:
        return word, phones

    # for hyphenated words, look up each word independently and then
    # join back up
    if "-" in word:
        phone_list = []
        for word in word.split('-'):
            suggested, phones = phones_for_word(word)
            phone_list.append((suggested, phones[0]))
        phones = [' '.join(p for (w, p) in phone_list if w)]
        word = '-'.join(w for (w, p) in phone_list)
        return word, phones

    else:
        return phones_for_closest_match(word)
    
# words = [
#     "mountain-side",
#     "nakedness",
#     "untrimm'd",
#     "factorize",
#     "duncan-phyfe",
#     "fuck-the-work-week",
#     "meat--attends",
#     "san'angelo",
#     'hiving-out"--and',
# ]
