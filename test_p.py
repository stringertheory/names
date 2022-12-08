import double_metaphone
import collections
import pronouncing
import editdistance

WORD = 'nakedness'
WORD = "untrimmed"
WORD = 'factorize'
WORD = 'obscurantism'
WORD = 'polyhedral'
WORD = 'moderna'

print(pronouncing.rhymes(WORD))

metaphone_to_word = collections.defaultdict(set)
for word in pronouncing.pronunciations:
    print(word)
    encoded = word.encode('utf8')
    for dm in double_metaphone.dm(encoded):
        if dm:
            metaphone_to_word[dm].add(word)
            
by_distance = []
for word in pronouncing.pronunciations:
    distance = editdistance.eval(word, WORD)
    if word.startswith(WORD[0]):
        distance -= 1
    if word.endswith(WORD[-1]):
        distance -= 1 
    character_difference = abs(len(word) - len(WORD))
    by_distance.append((distance, character_difference, word))

by_distance.sort()
print(by_distance[:100])
print(min(by_distance))
            
print(pronouncing.phones_for_word('luteous'))
print(pronouncing.phones_for_word('gluteus'))

possible = set()
for dm in double_metaphone.dm('luteous'):
    if dm:
        possible.update(metaphone_to_word['LTS'])

print(possible)


