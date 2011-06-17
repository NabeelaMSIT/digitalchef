from os import path

foodwords = []

def isfood(word):
	"""
	Return if the word is in the list of things which are recognised as ingredients
	"""
	global foodwords
	if not foodwords:
		f = open(path.join(path.dirname(path.abspath(__file__)), "food_words.txt"), "r")
		foodwords = [word.strip() for word in f.readlines()]
		print "food words", foodwords
	return (word in foodwords)
