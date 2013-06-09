import pyPdf
import nltk
import sys
import cPickle as pickle

filename = '/Users/heckj/Dropbox/games/Traveller5/Master Traveller5.pdf'
pdf = pyPdf.PdfFileReader(open(filename,"rb"))

offsets_map = {}
# offset_map: key is  - want a lookup to give a page num from an offset
# list instead (single pass over list to find)
# - damnit. tokens are just strings, so can't have additional attributes
# page_num = > offset_stop
master_tokens = []
offset = 0
for page_num in range(0, pdf.getNumPages()):
    print "processing page ", page_num
    pdf_page = pdf.getPage(page_num)
    raw_string = pdf_page.extractText()
    tokens = nltk.WordPunctTokenizer().tokenize(raw_string)
    master_tokens.extend(tokens)
    top_of_offsets = offset + len(tokens)
    offsets_map[page_num] = top_of_offsets

token_list_file = 'all_tokens.pickle'
offsets_file = 'token_offsets.pickle'
pickle.dump(master_tokens, open(token_list_file, 'wb'))
pickle.dump(offsets_map, open(offsets_file, 'wb'))

sys.exit(0)

# NOTE(heckj): the ConcordanceIndex doesn't have a means of tracking to
# additional metadata about the tokens built in  stock, so I'm tracking
# the additional information *alongside* the setup with a mapping of
# token offsets (which ConcordanceIndex returns) to page numbers.

print "There are %d words in the map" % len(token_map)
print "building text"
overall_text = nltk.Text(master_tokens)

print "---------- 100 collocations -----------"
overall_text.collocations(num=500)
print "---------- ---------------- -----------"

print overall_text.concordance('Imperium')

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

