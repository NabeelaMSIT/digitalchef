"""Models for the recipes app"""
#By Robert Miles

from django.db import models
from tagging.models import Tag
from django.contrib.auth.models import User, AnonymousUser


# Create your models here.
class Recipe(models.Model):
	"""The model for a recipe object"""
	title = models.CharField(max_length=200)	# The title of the recipe
	uploader = models.ForeignKey(User, default=-1, related_name="uploaded_recipes", editable=False)
	ingredients = models.TextField()
	instructions = models.TextField(blank=True)
	image_url = models.TextField(blank=True)	# Url to a photo of the dish
	
	def _get_tags(self):
		"return all tags associated with this object (thus all ingredients in this recipe)"
		return Tag.objects.get_for_object(self)

	def _set_tags(self, tag_list):
		"set the ingredients to all the names in the tag_list"
		Tag.objects.update_tags(self, tag_list)

	tags = property(_get_tags, _set_tags)	# properties map getters and setters to a variable

	def get_absolute_url(self):
		"""Ask the recipe for the url to view it"""
		return "/recipe/%s/" % self.id

	def __unicode__(self):
		"Called implicitly when you try and print a Recipe object"
		return self.title
        

