#profiles models
#By Robert Miles

from django.db import models
from django.contrib.auth.models import User

GENDER_CHOICES = (('M', 'Male'),('F', 'Female'))

class Profile(models.Model):
        """Object for user-editable information about Users"""
        user = models.ForeignKey(User, editable=False, unique=True,related_name="profile")
        about = models.TextField(null=True, blank=True)
        gender = models.CharField(max_length=1, choices=GENDER_CHOICES, null=True, blank=True)
        
        def get_absolute_url(self):
                return self.user.get_absolute_url()
        
        def __unicode__(self):
                return '[Profile] %s' % self.user.get_full_name()

