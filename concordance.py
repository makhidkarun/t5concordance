import nltk
from flask import Flask
from flask import render_template
from flask import g
import cPickle as pickle

app = Flask(__name__)
app.config['DEBUG'] = True


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

    # load up the offsets mapping for pagenumbers
    if hasattr(g, 'offsets'):
        offsets = g.offsets
    else:
        with app.open_resource('static/token_offsets.pickle') as f:
            app.logger.debug('loading offsets')
            offsets = pickle.load(f)
            g.offsets = offsets

    # load or build the ConcordanceIndex
    if hasattr(g, 'concord_index'):
        concord_index = g.concord_index
    else:
        concord_index = nltk.text.ConcordanceIndex(
            tokens, key=lambda s: s.lower())
        g.concord_index = concord_index

    result_map = {}
    if searchword:
        offsets = concord_index.offsets(searchword)
        if offsets:
            for i in offsets:
                token_context = ' '.join(concord_index._tokens[i-10:i+10])
                result_map[i] = token_context

    return render_template('base.html',
                           searchword=searchword,
                           results=result_map)
