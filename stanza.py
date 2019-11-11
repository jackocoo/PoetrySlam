

from PyDictionary import PyDictionary
from Phyme import Phyme
import nltk
import random
import os

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


def get_word_web(start_word):

	ph = Phyme()

	love_rhymes = ph.get_perfect_rhymes(start_word)

	list_single = love_rhymes[1];
	#print(love_rhymes)

	word_web = {}
	ants = []

	
	for word in list_single:
	
		syns = wordnet.synsets(word)
		associated_words = {}
		associated_words["v"] = []
		associated_words["n"] = []
		associated_words["s"] = []
		associated_words["a"] = []
		associated_words["r"] = []

		for l in syns:
			arr = l.name().split(".")
			results = associated_words[arr[1]]
			results.append(l.lemmas()[0].name())
			associated_words[arr[1]] = results
			if len(l.hypernyms()) > 0:
				for hyp in l.hypernyms():
					arr = hyp.name().split(".")
					results = associated_words[arr[1]]
					results.append(hyp.lemmas()[0].name())
					associated_words[arr[1]] = results
			if len(l.hyponyms()) > 0:
				for hyp in l.hyponyms():
					arr = hyp.name().split(".")
					results = associated_words[arr[1]]
					results.append(hyp.lemmas()[0].name())
					associated_words[arr[1]] = results
			for syn in l.lemmas():
				if syn.antonyms():
					ants.append(syn.antonyms()[0].name())
		word_web[word] = associated_words
	word_web["antonyms"] = ants
	return word_web


def make_new_line(diction, word):

	v_set = set()
	n_set = set()

	vowels = {"a", "A", "e", "E", "i", "I", "o", "O", "u", "U"}


	random_verbs = ["is", "are", "go", "goes", "has", "have"]
	random_nouns = ["it", "they", "he", "she"]
	preps = ["to", "for", "from", "of", "before", "after", "beside", "above", "through", "by"]
	conjunctions = ["and", "but", "yet"]

	verb = ""
	noun = ""
	prep = ""

	associated_verbs = diction[word]["v"]
	associated_nouns = diction[word]["n"]

	rand_verb = False
	rand_noun = False

	if len(associated_verbs) == 0:
		index = random.randrange(0, len(random_verbs), 1)
		rand_verb = True
		verb = random_verbs[index]

	else:
		index = random.randrange(0, len(associated_verbs), 1)
		verb = associated_verbs[index]


	if len(associated_nouns) == 0:
		index = random.randrange(0, len(random_nouns), 1)
		rand_noun = True
		noun = random_nouns[index]

	else:
		index = random.randrange(0, len(associated_nouns), 1)
		noun = associated_nouns[index]

	index = random.randrange(0, len(preps), 1)
	prep = preps[index]

	verb = verb.replace("_", " ")
	noun = noun.replace("_", " ")

	article = ""
	if rand_noun == False:
		char = noun[0]
		if char in vowels:
			article = "an"
		else:
			article = "a"

	if len(article) == 0:
		result = noun + " " + verb + " " + prep + " " + word
	else:
		result = article + " " + noun + " " + verb + " " + prep + " " + word

	if rand_verb == True and rand_noun == True:
		return ""
	return result


def print_lines(web):
	for key in web.keys():
		if key != "antonyms":
			string = make_new_line(web, key)
			print(string)
			string = "'" + string + "'"
			os.system("say " + string)




def main():
	web = get_word_web("love")
	ants = web["antonyms"]
	print_lines(web)
	if len(ants) == 0:
		new_word = "death"
	else:
		new_word = ants[0]
	#web2 = get_word_web(new_word)
	#print_lines(web2)
	string = "Thanks for listening"
	string = "'" + string + "'"

	os.system("say " + string)


main()




