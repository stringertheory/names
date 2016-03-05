import string
import syllable_count
import countsyl
import syllables_en
import pronouncing

def syllables(word):
    count = 0
    vowels = 'aeiouy'
    word = word.lower().strip(".:;?!")
    if word[0] in vowels:
        count +=1
    for index in range(1,len(word)):
        if word[index] in vowels and word[index-1] not in vowels:
            count +=1
    if word.endswith('e'):
        count -= 1
    if word.endswith('le'):
        count+=1
    if count == 0:
        count +=1
    return count

def sylcount(text):
    exclude = list(set(string.punctuation))
    count = 0
    vowels = 'aeiouy'
    text = text.lower()
    text = "".join(x for x in text if x not in exclude)
    
    if text == None:
	return 0
    elif len(text) == 0:
	return 0
    else:
	if text[0] in vowels:
	    count += 1
	for index in range(1, len(text)):
	    if text[index] in vowels and text[index-1] not in vowels:
		count += 1
	if text.endswith('e'):
	    count -= 1
	if text.endswith('le'):
	    count += 1
	if count == 0:
	    count += 1
        print text, count
	return count

def my(word):
    phones = pronouncing.phones_for_word(word)
    if phones:
        return pronouncing.syllable_count(phones[0])
    else:
        return syllables_en.count(word)
    
overallCorrect = overallTotal = 0
for i in range(1, 7):
    with open("%s-syllable-words.txt" % i) as f:
        words = f.read().split()
        for word in words:
            c = my(word)
            if c != i:
                print word, i, c
        correct = sum(my(word) == i for word in words)
    total = len(words)
    print("%s: %s correct out of %s (%.2f%%)" % (i, correct, total, 100*correct/total))
    overallCorrect += correct
    overallTotal += total

print()
print("%s correct out of %s (%.2f%%)" % (overallCorrect, overallTotal, 100*overallCorrect/overallTotal))
