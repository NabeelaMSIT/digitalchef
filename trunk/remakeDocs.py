#!/usr/bin/python

import os

PATH = os.path.abspath(os.path.dirname(__file__))

ppath = os.path.join(PATH, '..')
docpath = os.path.join(PATH, 'docs/html')

# big 'ol command line to run epydoc with all the right settings. Won't work on windows but I don't care.
os.system("PYTHONPATH=\"%s\" DJANGO_SETTINGS_MODULE=digichef.settings epydoc --html --parse-only --docformat plaintext re -v -o \"%s\" --graph all digichef" % (ppath, docpath))
