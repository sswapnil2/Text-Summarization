from __future__ import absolute_import
from __future__ import division, print_function, unicode_literals
from nltk.corpus import stopwords

from nltk.tokenize import word_tokenize
import urllib
from bs4 import BeautifulSoup
from nltk.tokenize import sent_tokenize

from collections import defaultdict

from heapq import nlargest
from string import punctuation


class TextSummarzation(object):

    def __init__(self, min_cut=0.1, max_cut=0.9, text = None, sent_tokens = None, n = 2):
        self._min_cut = min_cut
        self._max_cut = max_cut 
        self._stopwords = set(stopwords.words('english') + list(punctuation) )
        self._text = text
        self.sent_tokens = sent_tokens
        self.n = n

    def compute_frequencies(self, word_sent):
        freq = defaultdict(int)
        for s in word_sent:
            for word in s:
                if word not in self._stopwords:
                    freq[word] += 1
        # frequencies normalization and fitering
        m = float(max(freq.values()))
        for w in freq.keys():
            freq[w] = freq[w]/m
            if freq[w] >= self._max_cut or freq[w] <= self._min_cut:
                del freq[w]
        return freq 

    def summarize(self):
        sents = sent_tokenize(self._text)
        word_sent = [word_tokenize(s.lower()) for s in sents]
        freq = defaultdict(int)
        word_tokens = word_tokenize(self._text)
        filtered_sentence = [w for w in word_tokens if not w in self._stopwords]
                
        for word in filtered_sentence:
            if freq[word] == 0:
                freq[word] = 1
            else:
                freq[word] += 1

        ranking = defaultdict(int)        
        for i,sent in enumerate(word_sent):
            for w in sent :
                if w in freq and w not in self._stopwords:
                    ranking[i] += freq[w]
            sents_idx = self.rank(ranking, self.n)    
            ar = [sents[j] for j in sents_idx]

        return ar
         
    def rank(self, ranking, n):
        return nlargest(n, ranking, key=ranking.get) 

    def sentence_tokens(self, text, n):
        self.sent_tokens = sent_tokenize(self._text)
        assert n <= len(self.sent_tokens)
        return self.sent_tokens

    def word_tokens(self):
        word_tokens = word_tokenize(self._text)
        return word_tokens

    def get_text_from_url(self, url):
        # for testing use this url
        # url = "http://news.bbc.co.uk/2/hi/health/2284783.stm"
        html = urllib.request.urlopen(url).read()
        soup = BeautifulSoup(html,"lxml")

        # kill all script and style elements
        for script in soup(["script", "style"]):
            script.extract()    # rip it out

        # get text
        text = soup.get_text()

        # break into lines and remove leading and trailing space on each
        lines = (line.strip() for line in text.splitlines())
        # break multi-headlines into a line each
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        # drop blank lines
        text = '\n'.join(chunk for chunk in chunks if chunk)
        self._text = text
        return text 

    def remove_stopwords(self):
        word_tokens = word_tokenize(self._text)
        filtered_sentence = [w for w in word_tokens if not w in self._stopwords]
        return filtered_sentence
        
        
# for testing purpose

if __name__=="__main__":
    ts = TextSummarzation()
    text = ts.get_text_from_url("http://news.bbc.co.uk/2/hi/health/2284783.stm")
    # print(text)
    print(ts.summarize())

    print(ts.sent_tokens) 








