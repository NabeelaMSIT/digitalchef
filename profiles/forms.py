"""Custom forms for the profiles app live here"""

# By Robert Miles based on example code from http://birdhouse.org

from django import forms
from django.forms import ModelForm

from django.contrib.auth.models import User
from models import Profile

class ProfileForm(ModelForm):
	"""
	A custom form to make editing a profile more powerful.

	Fields like email and name are part of the User object, not the user's profile,
	so they cannot be edited with the default profile edit form. This custom
	form adds these extra fields
	"""

	def __init__(self, *args, **kwargs):
		"""Fill in the extra fields with the right dat afrom the user object"""
		super(ProfileForm, self).__init__(*args, **kwargs)
		try:
			#assert False, self.fields
			self.fields['email'].initial = self.instance.user.email
			self.fields['first_name'].initial = self.instance.user.first_name
			self.fields['last_name'].initial = self.instance.user.last_name
		except User.DoesNotExist:
			pass

	email = forms.EmailField(label="Primary email",help_text='')
	first_name = forms.CharField(label="First Name",help_text='')
	last_name = forms.CharField(label="Last Name",help_text='')

	class Meta:
		model = Profile
		exclude = ('user',)#The user shouldn't be able to change what user the profile associates with

	def save(self, *args, **kwargs):
		"""Update the email address and name on the related User object as well."""
		u = self.instance.user
		u.email = self.cleaned_data['email']
		u.first_name = self.cleaned_data['first_name']
		u.last_name = self.cleaned_data['last_name']
		u.save()
		profile = super(ProfileForm, self).save(*args,**kwargs)
		return profile
