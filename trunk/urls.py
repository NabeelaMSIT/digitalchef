#main urls.py
#By Robert Miles

from django.conf.urls.defaults import *
import recipes.views
import core
import util
import settings


from django.views.generic.simple import *

from django.views.generic.create_update import create_object
import recipes.models

from voting.views import vote_on_object


from digichef.profiles.forms import ProfileForm
from digichef.recommender.managers import RecommenderManager
from digichef.recipes.models import Recipe
from django.contrib.auth.models import User

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

man = RecommenderManager()

urlpatterns = patterns(
'',
#'django.views.generic.simple',

	(r'^admin/doc/', include('django.contrib.admindocs.urls')),
	(r'^admin/(.*)', admin.site.root),

	(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_DOC_ROOT, 'show_indexes': True}), 


    url(r'^$', 'core.views.home', name="home" ),

    url(r'^about/?$', 'django.views.generic.simple.direct_to_template', {'template':'about.html'}, name="about" ),

    (r'^search/?$','django.views.generic.simple.redirect_to', {'url': '/', 'permanent': False}),
    (r'^search/(?P<search_string>.*).*$', recipes.views.collab_search),

    url(r'^api/search$', recipes.views.api_collab_search, name="api_collab_search"),
    url(r'^api/similar/(?P<recipe_id>\d+)(/(?P<number>\d+))?$', recipes.views.api_similar_recipes, name="api_similar"),
    url(r'^api/recommended/(?P<username>\w+)(/(?P<number>\d+))?$', recipes.views.api_recommended_recipes, name="api_recommended"),
    url(r'^api/json_tags$', 'util.views.json_tags', name="json_tags"),

    url(r'^testing$', 'recipes.views.test', name="test"),

#	(r'^accounts/', include('registration.backends.default.urls')),
	(r'^accounts/', include('registration.urls')),


    ('^profiles/edit', 'profiles.views.edit_profile', {'form_class': ProfileForm,}),
    (r'^profiles/', include('profiles.urls')),
    (r'^users/(?P<username>\w+)/?$','django.views.generic.simple.redirect_to', {'url': '/profiles/%(username)s', 'permanent': False}),

#	url(r'^recipes/(?P<object_id>\d+)/(?P<direction>up|down|clear)vote/?$', vote_on_object, {'model':recipes.models.Recipe, 'template_object_name':'recipe', 'allow_xmlhttprequest':'true'}, name="recipe_voting"),
	url(r'^recipes/(?P<object_id>\d+)/(?P<direction>up|down|clear)vote/?$', recipes.views.vote_on_recipe, name="recipe_voting"),
 

    url(r'^recipe/tag/(?P<recipe_id>\d+)$', recipes.views.recipe_tag, name="recipe_tag"),
    (r'^recipe/(?P<recipe_id>\d+).*$', recipes.views.recipe_detail),


#    (r'^recipes/new/?$', recipes.views.create_recipe, {'template_name': 'recipes/recipe_new.html', 'login_required': True}),
    (r'^recipes/new/?$', create_object, {'model': recipes.models.Recipe,'template_name': 'recipes/recipe_new.html', 'login_required': True}),

    (r'^recipes/?$', recipes.views.recipes_all),
    (r'^recipes/all?$', recipes.views.recipes_all),
    (r'^recipes/by-rating?$', recipes.views.recipes_by_rating),
)
