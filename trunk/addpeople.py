"""To run this just import `addpeople` it from `python manage.py shell`"""

# By Robert Miles

from digichef.profiles.models import Profile
from digichef.recipes.models import Recipe
from digichef.voting.models import Vote
from django.contrib.auth.models import User

##### EDIT THIS BIT TO CHANGE USERS

people_list = [
	{	'username':		'rob',
		'first_name':	'Rob',
		'last_name':	'Miles',
		'is_superuser':	1,
		'is_staff':		1,
		'email':		"afromonkey0@gmail.com",
		'password':		"iamrob",

		'gender':		'M',
		'about':		"""I am the Technical Head of the DigiChef Project. I don't really like to cook that much but I need to have an account""",

		'likes':		['penguin', 'sushi', 'alfredo'], #strings in the title of liked recipes
		'dislikes':		['pork', 'beef', 'chicken'],
	},

	{	'username':		'dhruv',
		'first_name':	'Dhruv',
		'last_name':	'Gairola',
		'is_superuser':	1,
		'is_staff':		1,
		'email':		"",
		'password':		"iamdhruv",

		'gender':		'M',
		'about':		"""I am the Manager of the DigiChef Project.""",

		'likes':		['chocolate', 'sweet', 'cake'], #i have randomly decided that you like desserts
		'dislikes':		['hot', 'spicy', 'jalapeno'],	#and dislike spicy things
	},


	# fiction people start here

	{	'username':		'storm',
		'first_name':	'Storm',
		'last_name':	'Jones',
		'is_superuser':	0,
		'is_staff':		0,
		'email':		"",
		'password':		"iamstorm",

		'gender':		'F',
		'about':		"""Cooking is about feeding the soul and being one with the beautiful earth. It's very important""",

		'likes':		['veget', 'organic', 'natural', 'free', 'healthy'],
		'dislikes':		['meat', 'pork', 'beef', 'chicken'],
	},

	{	'username':		'batman',
		'first_name':	'Batman',
		'last_name':	'',
		'is_superuser':	0,
		'is_staff':		0,
		'email':		"",
		'password':		"iambatman",

		'gender':		'M',
		'about':		"""Ever since my parents were brutally murdered I've had to cook for myself, and I don't have much time to spare between beating the villains of Gotham City to a pulp. I mostly make stir fry.""",

		'likes':		['stir'],
		'dislikes':		[],
	},

	{	'username':		'chef',
		'first_name':	'Swedish',
		'last_name':	'Chef',
		'is_superuser':	0,
		'is_staff':		0,
		'email':		"",
		'password':		"iamchef",

		'gender':		'M',
		'about':		"""I cun't stup eateeng thuse-a demn Svedeesh Feesh!!""",

		'likes':		['meatball', 'swedish', 'sweden'],
		'dislikes':		[],
	},
	
	
	{	'username':		'amy',
		'first_name':	'Amy Jane',
		'last_name':	'Wesson',
		'is_superuser':	1,
		'is_staff':		1,
		'email':		"psycrajw@nottingham.ac.uk",
		'password':		"iamamy",

		'gender':		'F',
		'about':		"""I am document head for the project DigiChef. I love chocolate and love to bake cakes :-)""",

		'likes':		['cake', 'chocolate'], #strings in the title of liked recipes
		'dislikes':		['pork'],
	},

]

#### DON'T EDIT PAST HERE unless you're sure #####

print "deleting auth database (or most of it)..."
users = User.objects.all()
for user in users:
	for recipe in user.uploaded_recipes.all():
		recipe.uploader=None;
	user.delete()
	assert Recipe.objects.filter(title__contains='p'), "after delete of %s" % user

print "Loading testing data into database..."

assert Recipe.objects.filter(title__contains='penguin'), "after people delete"

for p in people_list:
	u = User(							# make the user
		username=p['username'],
		first_name=p['first_name'],
		last_name=p['last_name'],
		is_superuser=p['is_superuser'],
		is_staff=p['is_staff'],
		email=p['email'],
		)
	u.save()
	u.set_password(p['password'])		#give them their password
	u.save()

	prof = Profile(user=u, about=p['about'], gender=p['gender']) #make the profile
	prof.save()

	print "Made", u

	for word in p['likes']:	#place upvotes. 
		print word
		for recipe in Recipe.objects.filter(title__contains=word):
			print recipe
			Vote.objects.record_vote(recipe, u, 1)
			print "Upvoted %s for" % recipe, u

	for word in p['dislikes']:
		for recipe in Recipe.objects.filter(title__contains=word):
			Vote.objects.record_vote(recipe, u, -1)
			print "Downvoted %s for" % recipe, u



assert Recipe.objects.filter(title__contains='penguin'), "at end"











