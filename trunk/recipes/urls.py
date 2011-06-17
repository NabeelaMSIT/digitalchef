import recipes
from django.conf.urls.defaults import *


urlpatterns = patterns('',
    (r'^/?(?P<recipe_id>\d+).*$', recipes.views.recipe_detail),

    (r'^/?$', recipes.views.recipes_all),
)
