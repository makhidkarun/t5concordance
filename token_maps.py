import pyPdf
import nltk
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
    print("processing page ", page_num)
    pdf_page = pdf.getPage(page_num)
    raw_string = pdf_page.extractText()
    tokens = nltk.WordPunctTokenizer().tokenize(raw_string)
    master_tokens.extend(tokens)
    offset += len(tokens)
    offsets_map[page_num] = offset

token_list_file = 'static/all_tokens.pickle'
offsets_file = 'static/token_offsets.pickle'
pickle.dump(master_tokens, open(token_list_file, 'wb'))
pickle.dump(offsets_map, open(offsets_file, 'wb'))

# NOTE(heckj): the ConcordanceIndex doesn't have a means of tracking to
# additional metadata about the tokens built in  stock, so I'm tracking
# the additional information *alongside* the setup with a mapping of
# token offsets (which ConcordanceIndex returns) to page numbers.
