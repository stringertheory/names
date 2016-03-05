import re
import collections

def parse_cmu(cmufh):
    """Parses an incoming file handle as a CMU pronouncing dictionary file.

    (Most end-users of this module won't need to call this function explicitly,
    as it's called internally by the :func:`init_cmu` function.)

    :param cmufh: a filehandle with CMUdict-formatted data
    :returns: a list of 2-tuples pairing a word with its phones (as a string)
    """
    pronunciations = collections.defaultdict(list)
    regexp = re.compile(r'\(\d\)$')
    for line in cmufh:
        line = line.strip().decode('latin1')
        if line.startswith(';'):
            continue
        word, phones = line.split("  ")
        word = regexp.sub('', word.lower())
        pronunciations[word.lower()].append(phones)
    return pronunciations

import sys
with open(sys.argv[1]) as infile:
    for i in parse_cmu(infile).iteritems():
        print i
