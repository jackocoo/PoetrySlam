

from Phyme import Phyme
from profanityfilter import ProfanityFilter

#import nltk
import random
import os
import sys

import nltk
import ssl

try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    pass
else:
    ssl._create_default_https_context = _create_unverified_https_context

from nltk.corpus import wordnet as wordnet


"""
	This function takes a single word and returns a dictionary of dictionaries of "associated" words. 
	The dictionary returned has keys which are perfect rhymes of the starting word. Each key has a value which
	is a list of words which are hypernyms or hyponyms of the key. Additionally, the key "antonyms" 
	refers to a list of antonyms to the starting word. 

"""
def get_word_web(start_word):

	ph = Phyme()
	perfect_rhymes = ph.get_perfect_rhymes(start_word)

	pf = ProfanityFilter()

	#gets one syllable perfect rhymes
	if 1 in perfect_rhymes:
		list_single_rhymes = perfect_rhymes[1]
	else:
		list_single_rhymes = perfect_rhymes[2]
	word_web = {}
	antonyms = []

	for word in list_single_rhymes:

		if pf.is_clean(word):

			syns = wordnet.synsets(word)
			associated_words = {}
			associated_words["v"] = [] #verb
			associated_words["n"] = [] #noun
			associated_words["s"] = [] 
			associated_words["a"] = [] #adjective
			associated_words["r"] = []
			associated_words["i"] = []

			for l in syns:
				arr = l.name().split(".")
				if len(arr[1]) == 1:
					results = associated_words[arr[1]]
					results.append(l.lemmas()[0].name())
					associated_words[arr[1]] = results
				if len(l.hypernyms()) > 0:
					for hyp in l.hypernyms():
						arr = hyp.name().split(".")
						if len(arr[1]) == 1:
							results = associated_words[arr[1]]
							results.append(hyp.lemmas()[0].name())
							associated_words[arr[1]] = results
				if len(l.hyponyms()) > 0:
					for hyp in l.hyponyms():
						arr = hyp.name().split(".")
						if len(arr[1]) == 1:
							results = associated_words[arr[1]]
							results.append(hyp.lemmas()[0].name())
							associated_words[arr[1]] = results
				for syn in l.lemmas():
					if syn.antonyms():
						antonyms.append(syn.antonyms()[0].name())
			word_web[word] = associated_words
	word_web["antonyms"] = antonyms
	return word_web


"""
	This function is what generates new lines for the poem. It is given a word_web 
	(the dictionary) and the specific key with which it is generating the line according to. 
	The lines follow a formt which is an article, a noun, a verb, a preposition, and the specific key. 
	In instances where there are not words in the dictionary to choose from, the system chooses a 
	generic noun/verb randomly from a list. 

"""
def make_new_line(dictionary, word):

	v_set = set()
	n_set = set()

	vowels = {"a", "A", "e", "E", "i", "I", "o", "O", "u", "U"}

	random_verbs = ["is", "are", "go", "goes", "has", "have", "can", "could", "may"]
	random_nouns = ["it", "they", "he", "she", "one"]
	preps = ["to", "for", "from", "of", "before", "after", "beside", "above", "through", "by", "with"]

	verb = ""
	noun = ""
	prep = ""
	adj = ""

	associated_verbs = dictionary[word]["v"] 
	associated_nouns = dictionary[word]["n"]
	associated_adj = dictionary[word]["a"]

	#shuffle to ensure new orders each time this is called for a specific key
	random.shuffle(associated_nouns)
	random.shuffle(associated_verbs)
	random.shuffle(associated_adj)

	#reflects whether or not a generic verb or noun was selected 
	generic_verb = False
	generic_noun = False

	if len(associated_adj) > 0:
		index = random.randrange(0, len(associated_adj), 1)
		adj = associated_adj[index]

	if len(associated_verbs) == 0:
		index = random.randrange(0, len(random_verbs), 1)
		generic_verb = True
		verb = random_verbs[index]
	else:
		index = random.randrange(0, len(associated_verbs), 1)
		verb = associated_verbs[index]


	if len(associated_nouns) == 0:
		index = random.randrange(0, len(random_nouns), 1)
		generic_noun = True
		noun = random_nouns[index]
	else:
		index = random.randrange(0, len(associated_nouns), 1)
		noun = associated_nouns[index]

	index = random.randrange(0, len(preps), 1)
	prep = preps[index]


	#some of the words in the library have underscores instead of spaces
	verb = verb.replace("_", " ")
	noun = noun.replace("_", " ")

	if len(associated_adj) > 0:
		noun = adj + " " + noun

	article = ""
	if generic_noun == False:
		char = noun[0]
		if char in vowels:
			article = "an"
		else:
			article = "a"

	if len(article) == 0:
		result = noun + " " + verb + " " + prep + " " + word
	else:
		result = article + " " + noun + " " + verb + " " + prep + " " + word

	if generic_verb == True and generic_noun == True:
		return ""

	return result


"""
	This function calls make_new_line() for each of the keys in the word_web dictionary. 
	This gives a line to each synonym for the original starting word. 
"""
def print_lines(web):
	lines = []
	keys = []
	for key in web.keys():
		if key != "antonyms":
			keys.append(key)

	#done to ensure randomness of order
	random.shuffle(keys)

	count = 0
	for key in keys:
			string = make_new_line(web, key)
			if len(string) > 0:
				lines.append(string)
				count += 1
			if count > 11:
				return lines
	return lines


"""
	This function find the antonym in the list that is least semantically similar to the 
	given word. It does this by using wordnet's wup_similarity() function which finds a path 
	from one word to another through synonyms (if possible). 

"""
def find_best_antonym(ant_list, word):
	best = 100;
	best_word = ""
	original = wordnet.synsets(word)
	original_syn = wordnet.synset(original[0].name()) #the word we have been given 
	for ant in ant_list:
		if ant != word:
			w1 = wordnet.synsets(ant)
			antonym_to_compare = wordnet.synset(w1[0].name()) #the antonym we are comparing it to 
			score = original_syn.wup_similarity(antonym_to_compare)
			if score != None and score < best:
				best = score
				best_word = w1[0].name()
	return best_word.split(".")[0]


"""
	This function takes two lists of lines and combines them into a poem. This function creates
	12 lines which are comprised of two smaller lines, one from each list. The lines are combined using
	the word "but" because the lines are created using (loose) antonyms and should have opposing themes. 
	A list of the 12 final lines is returned. 
"""
def synthesize_antonym_components(list1, list2):
	result = []
	long_one = []
	short_one = []

	if len(list1) >= len(list2):
		long_one = list1
		short_one = list2
	else:
		long_one = list2
		short_one = list1

	count = 0;
	for i in range(0, len(short_one)):
		string = short_one[i] + " but " + long_one[i]
		result.append(string)
		count += 1
		if count > 11:
			break
	return result



"""	
	This function evaluates and score a poem on certain criteria. Poems that have greater alliteration, 
	greater semantic similarities between the first and second parts of each line, respectively, and 
	greater semantic differences between the first and second halves of each line will receive higher scores. 
	The final score is simply a sum of each of the subcategories. 

"""
def evaluate_poem(poem_lines):
	alliteration_score = 0
	contradiction_score = 0
	similarity_score = 0

	for line in poem_lines:
		first_half = line.split("but")[0]
		second_half = line.split("but")[1]

		split_words = line.split(" ")

		letter_set = set()
		for word in split_words:
			letter_set.add(word[0].lower())
		alliteration_score += 12 - len(letter_set) #higher score when first letters are repeated 



	return alliteration_score



"""
	This function puts together the above functions, taking an input word as the starting word, 
	making the word_web associated with it and its best antonym, then synthesizing the lines, and
	evaluating the poem. The poem will regenerate from the same web until it reaches a score above
	a certain threshold. Then the function will return that poem 
	
"""
def make_poem(starting_word):
	start_web = get_word_web(starting_word)
	start_lines = print_lines(start_web)
	antonym = find_best_antonym(start_web["antonyms"], starting_word)
	if len(antonym) == 0:
		antonym = "dark"

	title = starting_word +  " vs. " + antonym
	ant_web = get_word_web(antonym)
	ant_lines = print_lines(ant_web)

	total_lines = synthesize_antonym_components(start_lines, ant_lines)

	score = evaluate_poem(total_lines)

	count = 0
	while score < 50:
		start_lines = print_lines(start_web)
		ant_lines = print_lines(ant_web)
		total_lines = synthesize_antonym_components(start_lines, ant_lines)
		score = evaluate_poem(total_lines)
		count += 1
		if (count > 10):
			score = 50

	print("score is " + str(score))
	total_lines.append(title)
	return total_lines



"""
	This function calls the function to make the poem with the given word, then prints the poem 
	and reads the poem aloud. 
"""
def main():

	word = sys.argv[1]
	poem = make_poem(word)

	title = poem[len(poem) - 1]
	count = 0
	print("			" + title + "\n")

	full_string = ""
	for line in poem:
		if line == title:
			break
		print(line)
		full_string += line + "." + "\n"
		count += 1
		if count % 4 == 0:
			print()
	print()

	full_string = "'" + full_string + "'"
	os.system("say " + full_string)


main()




