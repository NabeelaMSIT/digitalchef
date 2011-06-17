#!/usr/bin/python
"""
Fill the recipe.image_url attributes with paths to hotlink to relevant images
as found by google image search
"""
import os

PATH = os.path.abspath(os.path.dirname(__file__))

# Make sure the user understands what's up
print """Don't do this too often since it uses User Agent Spoofing and
scraping of live pages as well as image hotlinking. This script is every 'do not'
rule of net etiquette and we don't want to piss off google more than we have to.
Well, maybe a bit more but we may wish to work there some day
"""
reply = raw_input("To go ahead with it anyway type 'yes': ")
#if they are sure
if reply == 'yes':
	ppath = os.path.join(PATH, '..')
	# Setting env variables on the command line doesn't work in windows, no solution for this as yet
	os.system("PYTHONPATH=\"%s\" DJANGO_SETTINGS_MODULE=digichef.settings python gimg.py" % ppath)

