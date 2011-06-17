#!/usr/bin/python
from urllib import urlopen
from BeautifulSoup import BeautifulSoup


def ask_tk_if_food(tagstring):
	"""Ask TrueKnowledge if it thinks the string is a type of food.

	Returns True or False
	This is quite prone to false negatives but has very few false positives.
	If it passes this, you can be pretty usre it's a valid ingredient"""

	query = "[%s][is a subclass of][food]" % tagstring
	url = "https://api.trueknowledge.com/query?query=query%%0A%s&api_account_id=api_rmiles&api_password=r8dmh8worl5c9xue" % query

	data = urlopen(url).read()
	bs = BeautifulSoup(data)

	if (bs.find("tk:status").string == "yes"):
		return True
	else:
		return False




if __name__ == "__main__":
	import sys
	print "Is %s food?\t%s" % (sys.argv[1], ask_tk_if_food(sys.argv[1]) and "yes" or "no")

