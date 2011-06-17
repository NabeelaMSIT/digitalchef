"""
This file is for local settings to make the project work on your machine.
To run the website locally for testing purposes, some settings will be different to how they are on the main server. So if you have to change a setting to make it work on your computer, change it in this file, it will override the setting in settings.py
DO NOT upload your own copy of this file to SVN, it will overwrite other peoples when they update their copies
"""

import os

WORKING_COPY = True
PATH = os.path.abspath(os.path.dirname(__file__))

## You probably shouldn't modify anything above this line ##

DATABASE_ENGINE = 'sqlite3'
DATABASE_NAME = os.path.join(PATH, 'dev.db')

MEDIA_ROOT = os.path.join(PATH, 'media')
STATIC_DOC_ROOT = os.path.join(PATH, 'media')
MEDIA_URL = '/media/'

#and to stop /media ur being grabbed by admin media
ADMIN_MEDIA_PREFIX = '/admin-media/'

TEMPLATE_DIRS = os.path.join(PATH, 'templates')

ABSOLUTE_URL_OVERRIDES = {
	'auth.user': lambda o: "/users/%s/" % o.username,
}

LOGIN_URL = '/accounts/login/'

LOGIN_REDIRECT_URL = '/'

LOGOUT_REDIRECT_URL = '/'

