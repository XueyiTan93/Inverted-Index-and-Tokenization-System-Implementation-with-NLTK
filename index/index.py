import xml.etree.ElementTree as ET
import string
import nltk
import argparse
from pathlib import Path
from collections import Counter
'''
# Path to your XML file
file_path = './index/20newsgroups-initial.xml'

# Parse the XML file
tree = ET.parse(file_path)

# Get the root element
root = tree.getroot()
# Iterate over each 'doc' element in the XML
for doc in root.findall('doc'):
    docid = doc.find('docid').text
    msgtext = doc.find('msgtext').text
    
    # Print out the extracted data
    print(f"Doc ID: {docid}")
    print(f"Message Text: {msgtext}")
    print("-" * 50)  # Print a separator
'''
class my_tokenizer:
    """tokenizer interface"""

    def __init__(self, contents):
        self.contents = contents

    def stem(self, contents):#method stem is an "abstract method" 
        """Tokenizer
        Args:
            text
        Returns:
            tokens
        """
        pass#pass does nothing SO the method isn't implemented.
    #the actual implementation of the stemming logic is expected to be provided by subclasses that inherit from the Stemmer class.

class ws_tokenizer(my_tokenizer): #child class of stemmer
    """whitespace tokenizer"""

    def __init__(self, contents):
        super().__init__(contents) #reference to the parent class
        self.contents = contents

    def tokenize(self, contents):#there is also def stem in parent class, so we are overriding stem as defined in parent class
        result=[]
        for i in self.contents.split(' '):
            result.append(i.lower().strip(string.punctuation))
        return result


"""a=ws_tokenizer(msgtext)#instantiation创建实例
print(a.tokenize(msgtext))"""

class nltk_tokenizer(my_tokenizer):
    """Off-the-shelf tokenizer from NLTK (Natural Language Toolkit)"""
    def __init__(self,contents):    
        super().__init__(contents)
        self.contents=contents

    def tokenize(self,contents):
        import nltk 
        result=[]
        for i in nltk.word_tokenize(self.contents):
            result.append(i.lower().strip(string.punctuation))
        return result

        #return nltk.word_tokenize(self.contents).lower().strip(string.punctuation)
    
"""b=nltk_tokenizer(msgtext)
print(b.tokenize(msgtext))"""



class n_gram_tokenizer(my_tokenizer):
    '''tokenize text into n-grams,where n is a parameter of that tokenizer function. The n-grams should be
taken over characters, not words.'''
    def __init__(self,contents,n=4):
        super().__init__(contents)
        self.contents=contents
    
    def tokenize(self,contents, n=4):
        low=[]
        for i in self.contents.split():
            low.append(i.lower().strip(string.punctuation))
        result=[]
        for i in low:
            if len(i)>=n:
                for j in range(len(i)-n+1):
                    result.append(i[j:j+n])
            else:
                result.append(i)
        return result

"""c=n_gram_tokenizer(msgtext)
print('default value =4:\n',c.tokenize(msgtext))
print('value =5:\n',c.tokenize(msgtext,5))
"""
#Stem the tokens using the Porter Stemmer from nltk.
def stem(tokens):
    '''input tokens(after tokenizer)'''
    from nltk.stem import PorterStemmer
    from collections import Counter
    stemmer = PorterStemmer()
    stemmed_tokens = [stemmer.stem(token) for token in tokens]
    return stemmed_tokens#return a list containing words after stemming

#Run this code in command line using:
#python index.py -f [path_to_collection] -t [tokenizer] -s [flag for whether to stem]
#python index.py -f '20newsgroups-initial.xml' -t whitespace -s
#The filepath of script and xml file should be relative to your current working directory
parser = argparse.ArgumentParser(description="Code to make inverted index")
parser.add_argument("-f", "--file", required=True,help="Path to the text file to be tokenized.")
parser.add_argument("-t", "--tokenizer", required=True, choices=['whitespace','nltk','n_gram'], 
                        help="The type of tokenizer to use ('whitespace' or 'nltk' or 'n_gram').")
parser.add_argument("-s", "--stem", action="store_true", 
                        help="Include this flag to enable stemming.")
args = parser.parse_args()

#file_path = './index/20newsgroups-initial.xml'

# Parse the XML file
tree = ET.parse(args.file)

# Get the root element
root = tree.getroot()
#Build the index
index=dict()

for doc in root.findall('doc'):
    docid = doc.find('docid').text
    text_body = doc.find('msgtext').text
    if args.tokenizer == 'whitespace':
        t=ws_tokenizer(text_body)
        list_of_tokens=t.tokenize(text_body)
    elif args.tokenizer == 'nltk':
        t=nltk_tokenizer(text_body)
        list_of_tokens=t.tokenize(text_body)
    elif args.tokenizer == 'n_gram':
        t=n_gram_tokenizer(text_body)
        list_of_tokens=t.tokenize(text_body)
    else:
        print(f"Invalid tokenizer: {args.tokenizer}")
        continue
    
    if args.stem ==True:
        list_of_tokens =stem(list_of_tokens)
    term_frequency=Counter(list_of_tokens)
    for token in term_frequency:
        if token in index:
            index[token] += [docid, term_frequency[token]]
        else:
            index[token] = [docid, term_frequency[token]]

print(index)#the completed index for 20newsgroups-initial.xml
#what document ids are returned for the query "system"(case-INsensitive)
print('query: system',index['system'])
print('query: compatibility',index['compat'])#
list_system=index['system']
list_com=index['compat']
intersection = [item for item in set(list_system) & set(list_com) if isinstance(item, str)]
print('query terms "system" and "compatibility"',intersection)#The result is ['8772', '14398']