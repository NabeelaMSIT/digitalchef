#util models
#By Robert Miles

from django.db import models
from django.contrib.auth.models import User
from digichef.voting.models import Vote
from digichef.recipes.models import Recipe

class UserMeta(models.Model):
	"""Object to store precomputed metadata about users"""
	user = models.ForeignKey(User, editable=False, unique=True,related_name="usermeta")
	votearraystr = models.TextField(null=True, blank=True)
	meanvote = models.FloatField()

	def update(self):
		votesdict = Vote.objects.get_for_user_in_bulk(Recipe.objects.all(), self.user)
		votes = []
		for i in xrange(Recipe.objects.count()):
			try:
				votes.append(votesdict[i].vote )
			except KeyError:#if there is no vote
				votes.append(0) #make it 0
		self.votearray = votes
		self.meanvote = (sum(votes)/float(len(votes)))

	def _get_votearray(self):
		return eval(self.votearraystr)

	def _set_votearray(self, newarray):
		self.votearraystr = str(newarray)

	votearray = property(_get_votearray, _set_votearray)

	def __unicode__(self):
		return '[userMeta] for %s' % self.user.get_full_name()

