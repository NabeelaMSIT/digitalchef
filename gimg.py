#!/usr/bin/python

from digichef.recipes.models import Recipe
from time import sleep

import os


for recipe in Recipe.objects.all():
	img_url = os.popen("""wget "http://images.google.com/images?q=%s&imgsz=m" -U Mozilla -q -O - | tidy -q 2>/dev/null | grep -i -m1 imgurl | egrep -o "http://[^&]+" | head -n1""" % recipe.title).read()
	print recipe.title,":",img_url[:40]
	recipe.image_url = img_url
	recipe.save()

