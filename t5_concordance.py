import nltk
import cPickle as pickle
import sys

token_list_file = 'static/all_tokens.pickle'
offsets_file = 'static/token_offsets.pickle'
master_tokens = pickle.load(open(token_list_file, 'rb'))
offsets_map = pickle.load(open(offsets_file, 'rb'))

# NOTE(heckj): the ConcordanceIndex doesn't have a means of tracking to
# additional metadata about the tokens built in  stock, so I'm tracking
# the additional information *alongside* the setup with a mapping of
# token offsets (which ConcordanceIndex returns) to page numbers.
#
# offsets_map[page_number] ==> last offset within that page

print "building text"
overall_text = nltk.Text(master_tokens)

print "---------- 100 collocations -----------"
overall_text.collocations(num=100)
print "---------- ---------------- -----------"

print overall_text.concordance('Imperium')
index = nltk.text.ConcordanceIndex(master_tokens, key=lambda s:s.lower())
sys.exit(0)

from nltk import bigrams
from nltk import collocations
from nltk import FreqDist
from nltk.collocations import BigramCollocationFinder

# http://nltk.googlecode.com/svn/trunk/doc/howto/collocations.html
# http://stackoverflow.com/questions/9151326/python-nltk-find-collocations-without-dot-separated-words
bigram_measures = collocations.BigramAssocMeasures()
word_fd = FreqDist(master_tokens)
bigram_fd = FreqDist(bigrams(master_tokens))
finder = BigramCollocationFinder(word_fd, bigram_fd)

#finder.apply_word_filter(lambda w: w in ('.', ','))
# only when collocation occurs 3+ times
finder.apply_freq_filter(3)

scored = finder.score_ngrams(bigram_measures.raw_freq)
#print sorted(bigram for bigram, score in scored)
print "========================================="
print sorted(finder.nbest(bigram_measures.raw_freq,200),reverse=True)

