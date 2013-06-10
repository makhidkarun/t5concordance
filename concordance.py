import nltk
from flask import Flask
from flask import render_template
from flask import g
import cPickle as pickle

app = Flask(__name__)
app.config['DEBUG'] = True

class ConcordanceResult(object):
    """A thingy to hold my concordance search results"""

    def __init__(self, offset):
        self.offset = offset

def _lookup_page_from_offset(offset_map, offset):
    """Returns a page number for the given offset."""
    # NOTE(heckj): Yes, I know this is an O(n) horrificness, worse with other
    # code that does iteration. Proper search indicies and such after this
    # whole thing is working.
    if offset_map is None or offset is None:
        return None
    keys = offset_map.keys()
    keys.sort()
    for page_num in keys:
        if offset_map[page_num] > offset:
            return page_num

@app.route('/')
@app.route('/<searchword>')
def frontpage(searchword=None):

    # load up the master token set
    if hasattr(g, 'tokens'):
        tokens = g.tokens
    else:
        with app.open_resource('static/all_tokens.pickle') as f:
            app.logger.debug('loading tokens')
            tokens = pickle.load(f)
            g.tokens = tokens
    assert(tokens)

    # load up the offsets mapping for pagenumbers
    if hasattr(g, 'offset_map'):
        offset_map = g.offset_map
    else:
        with app.open_resource('static/token_offsets.pickle') as f:
            app.logger.debug('loading offsets')
            offset_map = pickle.load(f)
            g.offset_map = offset_map
    assert(offset_map)

    # load or build the ConcordanceIndex
    if hasattr(g, 'concord_index'):
        concord_index = g.concord_index
    else:
        concord_index = nltk.text.ConcordanceIndex(
            tokens, key=lambda s: s.lower())
        g.concord_index = concord_index
    assert(concord_index)

    results = []
    if searchword:
        offsets = concord_index.offsets(searchword)
        if offsets:
            for i in offsets:
                a_result = ConcordanceResult(i)
                near_context = ' '.join(concord_index._tokens[i-10:i+10])
                a_result.context = near_context
                a_result.page_num = _lookup_page_from_offset(offset_map, i)
                results.append(a_result)

    return render_template('base.html',
                           searchword=searchword,
                           results=results)
