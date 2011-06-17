#core views

from digichef.recipes.models import Recipe
from digichef.tagging.models import Tag, TaggedItem
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext

def home(request):
	loginform = AuthenticationForm()
	slideshow_recipes = Recipe.objects.order_by('?')[:7]
	number_of_recipes = Recipe.objects.count()
	showcase_user = User.objects.order_by('?')[:1][0]

	return render_to_response('index.html', locals(), RequestContext(request))
