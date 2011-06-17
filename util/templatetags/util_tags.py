"""Extra tags for custom template behaviours live here"""

#By Robert Miles based on example code from http://gnuvince.wordpress.com/

from django import template

register = template.Library()


@register.simple_tag
def current(request, pattern):
	"""Return either 'current' or '' depending on if the current url matches the regex pattern"""
	import re
	if re.search(pattern, request.path):
		return 'current'
	return ''

@register.filter
def truncatechars(value, arg):
	"""truncate after a certain number of characters"""
	if len(value) < arg:
		return value
	else:
		return value[:arg] + '...'
