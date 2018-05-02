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

    def __init__(self, min_cut=0.1, max_cut=0.9):
        self._min_cut = min_cut
        self._max_cut = max_cut
        self._stopwords = set(stopwords.words('english') + list(punctuation))
        # print(self._stopwords)
        self.n = 4

    def _compute_frequencies(self, word_sent):

        freq = defaultdict(int)
        for s in word_sent:
            for word in s:
                if word not in self._stopwords:
                    freq[word] += 1
        # frequencies normalization and fitering
        m = float(max(freq.values()))
        new_freq = defaultdict(int)
        for w in freq.keys():
            freq[w] = freq[w]/m
            if freq[w] >= self._max_cut or freq[w] <= self._min_cut:
                # del freq[w]
                new_freq[w] = freq[w]
                pass
        return new_freq

    def summarize(self):

        sents = sent_tokenize(self._text)
        assert self.n <= len(sents)
        word_sent = [word_tokenize(s.lower()) for s in sents]
        self._freq = self._compute_frequencies(word_sent)
        ranking = defaultdict(int)
        for i, sent in enumerate(word_sent):
            # print(sent)
            for w in sent:
                if w in self._freq:
                    ranking[i] += self._freq[w]
        sents_idx = self._rank(ranking, self.n)
        return [sents[j] for j in sents_idx]

    def _rank(self, ranking, n):

        return nlargest(n, ranking, key=ranking.get)

    def remove_stopwords(self):
        return r = [w for w in self._text if w not in self._stopwords]

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
        text = ' '.join(chunk for chunk in chunks if chunk)
        self._text = text
        return text 

if __name__ == "__main__":
    ts = TextSummarzation()
    text = ts.get_text_from_url(
        "http://news.bbc.co.uk/2/hi/health/2284783.stm")
    # print(text)
    print(ts.summarize())

    # print(ts.sent_tokens)
