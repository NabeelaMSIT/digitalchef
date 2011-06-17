#recipes/views.py

from django.http import HttpResponse
from models import Recipe
from django.shortcuts import render_to_response, get_object_or_404
from django.db.models import Q
from digichef.tagging.models import Tag, TaggedItem
from digichef.recommender.managers import RecommenderManager
from django.template import RequestContext
from digichef.voting.models import Vote
from django.contrib.auth.models import User
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.views.generic.simple import redirect_to
from voting.views import vote_on_object
from digichef import simplejson

from digichef.util.models import UserMeta
import digichef.util.models

import re

from django.views.generic.create_update import create_object

def stupid_search(request):
	"""Search page"""
	if request.GET.get('submitted', ''):#if this a form submit;-
		#load the results of the select boxes into variable
		ingredient1 = request.GET.get('ingredient1', '')
		ingredient2 = request.GET.get('ingredient2', '')
		ingredient3 = request.GET.get('ingredient3', '')
		
		qset = (Q(name=ingredient1) | Q(name=ingredient2) | Q(name=ingredient3))
		search_ingreds = Tag.objects.filter(qset)#get the actual tags, not just their names

		# any
		recipes = TaggedItem.objects.get_union_by_model(Recipe, search_ingreds)
		#all
#		recipes = TaggedItem.objects.get_intersection_by_model(Recipe, search_ingreds)

		return recipe_list(request, recipes)

	else:#it's not a form submit, show the empty form
		all_ingreds = Tag.objects.all() #the select boxes need to know what ingreds there are
		return render_to_response('index.html', {'ingredients':all_ingreds}, RequestContext(request))

def api_similar_recipes(request, recipe_id, number):
	if not number:
		number = 5
	else:
		number = int(number)
	man = RecommenderManager()
	similar_recipes = man.get_by_relevance_to_tags(Recipe.objects.get(id=recipe_id).tags, Recipe.objects.exclude(id=recipe_id) ,0)
	similar_recipes.sort()
	similar_recipes.reverse()
	similar_recipes = [{'title':	recipe.title,
						'url':		recipe.get_absolute_url(),
						'img_url':	recipe.image_url,
					} for rating, recipe in similar_recipes[:number]]

	json = simplejson.dumps(similar_recipes)
	return HttpResponse(json, mimetype="application/json")

def api_recommended_recipes(request, username, number):
	if not number:
		number = 5
	else:
		number = int(number)
	man = RecommenderManager()

	recommended_recipes = man.get_recommendations_for_user_on_items(User.objects.get(username=username), Recipe.objects.all(), number)
	recommended_recipes.sort(reverse=True)
	recommended_recipes = [{'title':	recipe.title,
						'url':		recipe.get_absolute_url(),
						'img_url':	recipe.image_url,
						'rating':	rating,
					} for rating, recipe in recommended_recipes[:number]]

	json = simplejson.dumps(recommended_recipes)
	return HttpResponse(json, mimetype="application/json")

def api_collab_search(request):
	if request.method == 'POST':
		q = request.POST.get('q', None)
		if q is not None:
			return redirect_to(request, url='/search/%s'%q)
		else:
			assert False, "This API method requires the post variable 'q', the query"
	else:
		assert False, "This API method requires POST data"

def recipe_tag(request, recipe_id):
	recipe = get_object_or_404(Recipe, pk=recipe_id)

	try:
		recipe.uploader
		has_uploader = True
	except:
		has_uploader = False		

	if request.user.is_authenticated() and \
			(request.user.is_staff or request.user.is_superuser or \
			(has_uploader and (recipe.uploader == request.user))):
		if request.method == 'POST':
			tags = request.POST.get('tags', None)
			if tags is not None:
				recipe.tags = tags
				return redirect_to(request, url='/recipe/%s/%s'%(recipe_id, tags))
			else:
				assert False, "This method requires the post variable 'tags'"
		else:
			return render_to_response('recipes/recipe_tag.html', {'recipe' : recipe})
	else:
		assert False, "To edit this recipe's tags you must own it or be an admin"


def collab_search(request, search_string):
	search_terms = [str(item.strip(',')) for item in re.split(r"[,; \t]*", search_string) if item]
	man = RecommenderManager()
	man = RecommenderManager()

	results = man.get_by_relevance_to_tags(search_terms, Recipe.objects.all(),0)

	results.sort(reverse=True)

	return recipe_list(request, [listing[1] for listing in results], search_terms)


def recipes_all(request):
        """View all recipes"""
        recipeSet = Recipe.objects.all().order_by('title')
        return recipe_list(request, recipeSet)

def recipes_by_rating(request):
	"""View all recipes ordered by their rating"""
	recipeSet = Vote.objects.get_scores_in_bulk(Recipe.objects.all())
	recipeSet = sorted([(recipeSet[elem]['score'], Recipe.objects.get(id=elem))for elem in recipeSet], reverse=True)
	return recipe_list(request, [item[1] for item in recipeSet])

def recipe_list(request, queryset, taglist=[]):
	"""View of a list of recipes"""

	paginator = Paginator(queryset, 25, orphans=3) # Show 25 contacts per page, min 3 per page

	# Make sure page request is an int. If not, deliver first page.
	try:
		page = int(request.GET.get('page', '1'))
	except ValueError:
		page = 1

	# If page request (9999) is out of range, deliver last page of results.
	try:
		recipes = paginator.page(page)
	except (EmptyPage, InvalidPage):
		recipes = paginator.page(paginator.num_pages)

	return render_to_response('recipe_list.html', {'recipes' : recipes, 'taglist':taglist})


def recipe_detail(request, recipe_id):
	"""View for a detailed look at a single recipe

		returns 404 error if recipe not found"""
	recipe = get_object_or_404(Recipe, pk=recipe_id)
	ingredient_list = recipe.ingredients.split("\n")
	score = Vote.objects.get_score(recipe)

	return render_to_response('recipe_detail.html', locals(), RequestContext(request))


def vote_on_recipe(request, object_id, direction):
	print "val", direction
	returnval = vote_on_object(request, Recipe, direction, object_id=object_id, template_object_name='recipe', allow_xmlhttprequest=True)
#	try:
#		try:
#			usermeta = UserMeta.objects.get(user__id=request.user.id)#
#		except:
#			usermeta = UserMeta(request.user)
#		print usermeta.votearray
#	except Exception as e:
#		print type(e), e
	return returnval

def create_recipe(request, *args, **kwargs):
	kwargs.update({'model': Recipe})
	assert False, (args, kwargs)

def test(request):
	objectType = Recipe
	man = RecommenderManager()
	user1 = User.objects.get(id=1)
	votes = man.get_pred_vote_for_user_on_items(user1, Recipe.objects.all())
#	votes = user1.usermeta.all()[0].votearray
	assert False, votes









