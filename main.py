

from PyDictionary import PyDictionary
from Phyme import Phyme
import nltk


import nltk
import ssl

try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    pass
else:
    ssl._create_default_https_context = _create_unverified_https_context

#nltk.download('wordnet')
from nltk.corpus import wordnet as wordnet


def main():

	input_word = "dream"

	ph = Phyme()
	result = ph.get_perfect_rhymes("DOG")
	print(result[1])

	#syns = wordnet.synsets("dog")


	synonyms = [] 
	antonyms = [] 
	  
	for syn in wordnet.synsets("dog"): 
	    for l in syn.lemmas(): 
	        synonyms.append(l.name()) 
	        if l.antonyms(): 
	            antonyms.append(l.antonyms()[0].name()) 

	print(synonyms)
	print(antonyms)


	  
	w1 = wordnet.synset('pet.n.01') # v here denotes the tag verb 
	w2 = wordnet.synset('dog.n.01') 
	print(w1.wup_similarity(w2)) 

main()




