# What does this code do

It's a python program to build an inverted index from xml file.

The output is an index dictionary containing all the words (maybe after stemming) and their doc_id, term_frequency in that doc_id.

For example:

'contact': ['15641', 1, '8082', 1], 'sunday': ['15641', 2],'justic': ['15641', 2], 'depart': ['15641', 2], ...

# How to run

Run this code in command line using:
python index.py -f [path_to_collection] -t [tokenizer] -s [flag for whether to stem]
python index.py -f '20newsgroups-initial.xml' -t whitespace -s
The filepath of script and xml file should be relative to your current working directory

You can query the index by： index['The_keyword_you_want_to_search'] (**The keyword must be ALL LOWERCASE!**)
index['system']