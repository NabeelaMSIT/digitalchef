#!/usr/bin/python
"""Wipe the database clean and add default data using loaddata.py.

If you get 'table doesn't exist' errors, run 'python manage.py syncdb'
If you get 'what the hell is PYTHONPATH' errors, you're running windows and this script won't work.
Working of a fix for that,
"""
import os

PATH = os.path.abspath(os.path.dirname(__file__))

# Make sure the user understands what's up
print """This will delete all data in the database
AND REPLACE IT WITH DEFAULT DATA!!!"
THE ONLY DATA LEFT WILL BE THAT SPECIFIED IN loaddata.py"
You lose anything else added later"
It should be noted that this isn't a joke"""
reply = raw_input("Are you seriously sure (type 'yes' to continue)? ")
#if they are sure
if reply == 'yes':
	os.system("python manage.py reset recipes tagging --noinput")# wipe DB
	ppath = os.path.join(PATH, '..')
	# Setting env variables on the command line doesn't work in windows, no solution for this as yet
	os.system("PYTHONPATH=\"%s\" DJANGO_SETTINGS_MODULE=digichef.settings python loaddata.py" % ppath)# fill with default data

