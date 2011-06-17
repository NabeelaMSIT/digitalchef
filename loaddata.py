#!/usr/bin/python

"""Dump a bunch of default data into the database for testing.
This file isn't meant to be run on its own, use remakeDatabase.py"""

import digichef

from digichef.recipes.models import *
from digichef.tagging.models import *

from django.contrib.auth.models import User

from digichef.util import isfood

def load_data():

	print "deleting auth database (or most of it)..."
	users = User.objects.all()
	#Cheers :)
	for user in users:
		user.delete()

	print "Loading testing data into database..."

	#===============PEOPLE======================

	p = User(
	username='rob',
	first_name='Rob',
	last_name='Miles',
	is_superuser=1,
	is_staff=1,
	email="afromonkey0@gmail.com"
	)
	p.save()
	p.set_password("iamrob")
	p.save()

	p = User(
	username='dhruv',
	first_name='Dhruv',
	last_name='Gairola',
	is_superuser=1,
	is_staff=1,
	email="" #idk
	)
	p.save()
	p.set_password("iamdhruv")
	p.save()
	

	#===============RECIPES======================

	DUMPXML = True

	if DUMPXML:

		from BeautifulSoup import BeautifulStoneSoup

		soup = BeautifulStoneSoup(open("recipes.xml", "r").read())

	#	print soup

		for recipe in soup.findAll("recipe"):
			try:
				ings = [ing.string for ing in recipe.ingredients.findAll("ingredient")]
				r = Recipe(
					title = recipe.title.string,
					ingredients = "\n".join(ings),
					instructions = recipe.instructions.string or ""
					)
				r.save()
				words = reduce(lambda x,y: x+y, [ing.split() for ing in ings])
				r.tags = " ".join([word for word in words if isfood(word)])
				print r, r.tags
			except:
				print recipe
	#			print type(recipe)
				raise


	else:
	
		r = Recipe(
		title='Blueberry Peach Muffins',
		ingredients="""375 g all-purpose flour
	100 g white sugar
	110 g brown sugar
	10 g baking powder
	1 g salt
	3 eggs
	235 ml milk
	115 g melted butter
	145 g blueberries
	170 g peeled and diced fresh peaches

	8 g white sugar
	2 g ground cinnamon
	2 g ground nutmeg
	30 g melted butter""",
		instructions="""Preheat the oven to 400 degrees F (200 degrees C). Grease muffin tins, or line with paper liners.
	In a large bowl, stir together the flour, 1/2 cup white sugar, brown sugar, baking powder and salt. In a  separate bowl, mix together the eggs, milk  and 1/2 cup of melted butter until well blended. Pour the wet ingredients into the dry, and mix until just blended. Fold in the blueberries and peaches. Fill muffin cups with batter.
	Bake for 18 to 20 minutes in the preheated oven, or until the tops spring back when lightly touched. In a small bowl, stir together the remaining sugar, cinnamon and nutmeg. Brush muffins with remaining melted butter, and sprinkle with the cinnamon mixture. Cool in the pan over a wire rack.""",
		)
		r.save()
		r.tags = 'brown_sugar baking_powder salt egg milk butter blueberry peach white_sugar cinnamon nutmeg'

		r = Recipe(
		title="Ferg's Ulster Fry-up",
		ingredients="""2 thick slices Irish bacon
	26 g sausages
	1 soda bread farl, sliced in half horizontally
	2 potato bread farls
	15 ml vegetable oil, or as needed
	2 slices black pudding
	1 tomato, halved
	2 eggs""",
		instructions="""Preheat oven to 300 degrees F (150 degrees C).
	In a large non-stick skillet over medium heat, cook the bacon and sausages, until they are browned.  Reserving the fat in the pan, transfer to a heat resistant dish. Keep warm in the oven.
	Fry both sides of the potato and soda farls in the reserved fat for a few minutes, or until they are golden and crispy. Meanwhile, heat oil in smaller skillet over medium heat and cook black pudding slices and tomato halves. Transfer everything to the dish in the oven to keep warm.
	Crack eggs into the pan with any residual bacon grease, adding more oil to the skillet if necessary.  Fry until egg whites are set but yolks are still runny, or to your liking. Divide everything onto 2 separate plates and serve immediately.""",
		)
		r.save()
		r.tags='bacon sausage farl oil black_pudding tomato egg'



		r = Recipe(
		title="World's Best Lasagna",
		ingredients="""455 g sweet Italian sausage
	340 g lean ground beef
	80 g minced onion
	2 cloves garlic, crushed
	1 (28 ounce) can crushed tomatoes
	2 (6 ounce) cans tomato paste
	364 g canned tomato sauce
	120 ml water
	25 g white sugar
	1 g dried basil leaves
	1 g fennel seeds
	2 g Italian seasoning
	20 g salt
	0.5 g ground black pepper
	15 g chopped fresh parsley
	12 lasagna noodles
	455 g ricotta cheese
	1 egg
	3 g salt
	340 g mozzarella cheese, sliced
	60 g grated Parmesan cheese""",
		instructions="""In a Dutch oven, cook sausage, ground beef, onion, and garlic over medium heat until well browned. Stir in crushed tomatoes, tomato paste, tomato sauce, and water. Season with sugar, basil, fennel seeds, Italian seasoning, 1 tablespoon salt, pepper, and 2 tablespoons parsley. Simmer, covered, for about 1 1/2 hours, stirring occasionally.
	Bring a large pot of lightly salted water to a boil. Cook lasagna noodles in boiling water for 8 to 10 minutes. Drain noodles, and rinse with cold water.  In a mixing bowl, combine ricotta cheese with egg, remaining parsley, and 1/2 teaspoon salt.
	Preheat oven to 375  degrees F (190 degrees C).
	To assemble, spread 1 1/2 cups of meat sauce in the bottom of a 9x13 inch baking dish.  Arrange 6 noodles lengthwise over meat sauce. Spread with one half of the ricotta cheese mixture. Top with a third of mozzarella cheese slices. Spoon 1 1/2 cups meat sauce over mozzarella, and sprinkle with 1/4 cup Parmesan cheese.  Repeat layers, and top with remaining mozzarella and Parmesan cheese. Cover with foil: to prevent sticking, either spray foil with cooking spray, or make sure the foil does not touch the cheese.
	Bake in preheated oven for 25 minutes. Remove foil, and bake an additional 25 minutes. Cool for 15 minutes before serving.""",
		)
		r.save()
		r.tags='sausage beef onion garlic tomato tomato_paste tomato_sauce water white_sugar basil fennel_seed salt black_pepper parsley pasta ricotta egg mozzarella parmesan'


		r = Recipe(
		title="Apple Pie by Grandma Ople",
		ingredients="""1 recipe pastry for a 9 inch double crust pie
	115 g unsalted butter
	25 g all-purpose flour
	60 ml water
	100 g white sugar
	110 g packed brown sugar
	8 Granny Smith apples - peeled, cored and sliced""",
		instructions="""Preheat oven to 425 degrees F (220 degrees C). Melt the butter in a saucepan. Stir in flour to form a paste. Add water, white sugar and brown sugar, and bring to a boil. Reduce temperature and let simmer.
	Place the bottom crust in your pan. Fill with apples, mounded slightly. Cover with a lattice work of crust.  Gently pour the sugar and butter liquid over the crust.  Pour slowly so that it does not run off.
	Bake 15 minutes in the preheated oven. Reduce the temperature to 350 degrees F (175 degrees C). Continue baking for 35 to 45 minutes, until apples are soft.""",
		)
		r.save()
		r.tags='pastry butter flour water white_sugar brown_sugar apple'

		r = Recipe(
		title="Chantal's New York Cheesecake",
		ingredients="""15 graham crackers, crushed
	30 g butter, melted

	896 g cream cheese
	300 g white sugar
	180 ml milk
	4 eggs
	230 g sour cream
	15 ml vanilla extract
	30 g all-purpose flour""",
		instructions="""Preheat oven to 350 degrees F (175 degrees C). Grease a 9 inch springform pan.
	In a medium bowl, mix graham cracker crumbs with melted butter. Press onto bottom of springform pan.
	In a large bowl, mix cream cheese with sugar until smooth. Blend in milk, and then mix in the eggs one at a time, mixing just enough to incorporate. Mix in sour cream, vanilla and flour until smooth. Pour filling into prepared crust.
	Bake in preheated oven for 1 hour. Turn the oven off, and let cake cool in oven with the door closed for 5 to 6 hours; this prevents cracking. Chill in refrigerator until serving.""",
		)
		r.save()
		r.tags='graham_crackers butter cream_cheese white_sugar milk egg sour_cream vanilla_extract flour'


		r = Recipe(
		title='Chicken Pot Pie',
		ingredients="""455 g skinless, boneless chicken breast halves - cubed
	120 g sliced carrots
	150 g frozen green peas
	60 g sliced celery
	75 g butter
	55 g chopped onion
	40 g all-purpose flour
	3 g salt
	0.5 g black pepper
	0.5 g celery seed
	415 ml chicken broth
	160 ml milk

	2 (9 inch)  unbaked pie crusts""",
		instructions="""Preheat oven to 425 degrees F (220 degrees C.)
	In a saucepan, combine chicken, carrots, peas, and celery. Add water to cover and boil for 15 minutes. Remove from heat, drain and set aside.
	In the saucepan over medium heat, cook onions in butter until soft and translucent. Stir in flour, salt, pepper, and celery seed. Slowly stir in chicken broth and milk. Simmer over medium-low heat until thick. Remove from heat and set aside.
	Place the chicken mixture in bottom pie crust. Pour hot liquid mixture over. Cover with top crust, seal edges, and cut away excess dough. Make several small slits in the top to allow steam to escape.
	Bake in the preheated oven for 30 to 35 minutes, or until pastry is golden brown and filling is bubbly. Cool for 10 minutes before serving.""",
		)
		r.save()
		r.tags='chicken carrot pea celery butter onion flour salt black_pepper celery_seed chicken_broth milk pie_crust'

		r = Recipe(
		title="Grilled Salmon",
		ingredients="""680 g salmon fillets
	lemon pepper to taste
	garlic powder to taste
	salt to taste
	80 ml soy sauce
	75 g brown sugar
	80 ml water
	60 ml vegetable oil""",
		instructions="""Season salmon fillets with lemon pepper, garlic powder, and salt.
	In a small bowl, stir together soy sauce, brown sugar, water, and vegetable oil until sugar is dissolved. Place fish in a large resealable plastic bag with the soy sauce mixture, seal, and turn to coat. Refrigerate for at least 2 hours.
	Preheat grill for medium heat.
	Lightly oil grill grate. Place salmon on the preheated grill, and discard marinade. Cook salmon for 6 to 8 minutes per side, or until the fish flakes easily with a fork.""",
		)
		r.save()
		r.tags='salmon lemon_pepper garlic_powder salt soy_sauce brown_sugar water vegetable_oil'


if __name__ == "__main__":
    load_data()



















