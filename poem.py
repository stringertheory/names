"""

http://www.theatlantic.com/past/docs/unbound/poetry/gioia/gioia.htm?src=longreads

https://www.wired.com/2016/11/poetry-popularity-on-twitter/
"""

class Poem(object):

    def __init__(self, document):
        self.document = document

    def iterpositions(self):
        analyzed = self.document.get('analyzed', [])
        for sentence_index, sentence in enumerate(analyzed):
            for word_index, word_obj in sentence:
                yield (sentence_index, word_index), word_obj
            
