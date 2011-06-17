from digichef.tagging.models import Tag, TaggedItem
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext

def homepage(request):
	loginform = AuthenticationForm()
	all_ingreds = Tag.objects.all()
	return render_to_response('index.html', {'ingredients':all_ingreds, 'loginform':loginform}, RequestContext(request))
