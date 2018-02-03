t5concordance
=============

A little playground for interactively poking at the T5 PDF's with NLTK to
find bigrams, trigrams, collocations, and poke at concordances.

Uses:
* pyPDF
* nltk
* virtualenv

Setup
-----

    virtualenv .venv --clear
    source .venv/bin/activate
    pip install -r requirements.txt

Make the token maps for concordances and such:

    python token_maps.py
    # ^^ hard coded location on my local system to where to find the PDF

Playground for interactively fiddling with nltk:

    python -i t5_concordance.py

This generates two files:
* token_offsets.pickle
* all_tokens.pickle

which is the result of scraping the pdf with pyPdf, tokenizing the
extracted text, and stashing the offsets to keep track of page numbers.
The list of tokens (in all_tokens.pickle) is what's needed by NLTLK
to build concordnace indicies and other interesting processing.

Copyright Notice
----------------

The Traveller game in all forms is owned by Far Future Enterprises.
Copyright 1977 - 2013 Far Future Enterprises. Traveller is a registered
trademark of Far Future Enterprises. Far Future permits web sites and
fanzines for this game, provided it contains this notice, that Far Future
is notified, and subject to a withdrawal of permission on 90 days notice.
The contents of this site are for personal, non-commercial use only. Any
use of Far Future Enterprise's copyrighted material or trademarks anywhere
in this repository and its files should not be viewed as a challenge to
those copyrights or trademarks.

All other content and contributions in this repository are under the
Apache 2.0 license (see LICENSE.txt)

Heroku App
----------

App URL http://t5concordance.herokuapp.com/
Git URL git@heroku.com:t5concordance.git

Note: to avoid publishing the entire tokenset of the T5 rules to github,
I've created a local branch named 'heroku' that includes the relevant
pickle files (created with make_maps.py) in the static/ directory. I then
push this branch as rebased and updated as needed to heroku to present
the application using:

    git push heroku heroku:master
