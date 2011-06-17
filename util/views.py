#util views

from django.shortcuts import render_to_response, get_object_or_404
from digichef.tagging.models import Tag

def json_tags(request):
	tags = Tag.objects.all()
	return render_to_response('api/tags.json', {'tags':tags})
