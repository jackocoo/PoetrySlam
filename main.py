

from PyDictionary import PyDictionary
from Phyme import Phyme
import nltk
import random

#import en

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

	preps = ["to", "for", "from", "of", "before", "after", "beside", "above"]
	fun_words = ["love", "loss", "pain", "joy", "fear", "death"]

	ph = Phyme()


	for wordy in fun_words:
		parent_word = wordy
		syns = wordnet.synsets(parent_word)
		boat = wordnet.synset(syns[0].name())
		rhymes = ph.get_perfect_rhymes(parent_word)
		entailments = boat.entailments()
		print(rhymes)
				#print(rhymes)

		#find the rhyming word that is the most contextually similar to the parent word 
		print("he he he")
		max_score = 0.0
		saver = syns[0].name()

		for num in rhymes.keys():
			for word in rhymes[num]:
				new_synset = wordnet.synsets(word)
				if len(new_synset) > 0 and parent_word != word:
					thing = wordnet.synset(new_synset[0].name())
					result = boat.wup_similarity(thing)
					if result != None and result > max_score:
						max_score = result
						saver = new_synset[0].lemmas()[0].name()


		print(max_score)
		print(saver)

		index = random.randrange(0, len(fun_words), 1)
		random_prep = preps[index];

		result_string = parent_word + " " + random_prep + " " + saver
		print("STRING IS " + result_string)



		print("he he he")

	"""
	synonyms = [] 
	  	  
	for syn in syns: 
	    for l in syn.lemmas(): 
	        synonyms.append(l.name()) 


	print(synonyms)


	  
	w1 = wordnet.synset('pet.n.01') # v here denotes the tag verb 
	w2 = wordnet.synset('dog.n.01') 
	print(w1.wup_similarity(w2)) 
	"""



main()




