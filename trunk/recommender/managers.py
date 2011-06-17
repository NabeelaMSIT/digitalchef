#recommender managers

from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import User

import utils

from voting.models import Vote
from tagging.models import Tag

from digichef.util.tools import poke, output

class RecommenderManager(models.Manager):

    MIN_RECOMMENDATION_VALUE = 0
    MIN_SIMILARITY_VALUE = 0.25
    MIN_CONTENT_BASED_RECOMMENDATION_VALUE = 0.25
    
    def get_best_items_for_user(self, user, user_list, item_list, min_value=MIN_RECOMMENDATION_VALUE):
        user_item_matrix = self.create_matrix(user_list, item_list)

        recs = utils.get_usb_recommendations(user.id, user_item_matrix)
        recs.sort(reverse=True)
        
        ctype = ContentType.objects.get_for_model(item_list[0])
        items = [(value,ctype.get_object_for_this_type(id = rec)) for value,rec in recs if value>min_value]
        return items
        
    def get_items_for_user(self, user, itemtype, min_value=MIN_RECOMMENDATION_VALUE):
        items_voted = Vote.objects.get_for_user_in_bulk(itemtype.objects.all(), user)
        items_liked = [vote.object for number, vote in items_voted.items() if vote.is_upvote()]
        items_disliked = [vote.object for number, vote in items_voted.items() if vote.is_downvote()]
        good_tags = set([])
        bad_tags = set([])
        for item in items_liked:
            for tag in item.tags:
                good_tags.add(tag)
        for item in items_disliked:
            for tag in item.tags:
                bad_tags.add(tag)
        tagset = good_tags-bad_tags
        return sorted(self.get_by_relevance_to_tags(tagset, itemtype.objects.all(), min_value), reverse=True)

        

    def get_similar_users(self, user, user_list, item_list, min_value=MIN_SIMILARITY_VALUE):
        user_item_matrix = self.create_matrix(user_list, item_list)
        sim_list = []
        for other in user_list:
            if user==other:continue
            sim=utils.distance_matrix_p1_p2(user_item_matrix[user.id],user_item_matrix[other.id]) #returns a 0..1 value
            if sim>min_value:
                sim_list.append((sim,other))
            
        sim_list.sort(reverse=True)
        return sim_list

    def get_best_users_for_item(self, item, user_list, item_list, min_value=MIN_RECOMMENDATION_VALUE):
        user_item_matrix = self.create_matrix(user_list, item_list)
        item_user_matrix = self.rotate_matrix(user_item_matrix)

        recs = utils.get_usb_recommendations(item.id, item_user_matrix)
        recs.sort(reverse=True)

        users = [(value,User.objects.get(id = rec)) for value,rec in recs if value>min_value]
        
        return users
    
    def get_similar_items(self, item, user_list, item_list, min_value=MIN_SIMILARITY_VALUE):
        user_item_matrix = self.create_matrix(user_list, item_list)
        item_user_matrix = self.rotate_matrix(user_item_matrix)
#	assert False, (user_item_matrix, item_user_matrix)
        sim_list = []
        for other in item_list:
            if item==other:continue
            sim=utils.distance_matrix_p1_p2(item_user_matrix[item.id],item_user_matrix[other.id]) #returns a 0..1 value
            if sim>min_value:
                sim_list.append((sim,other))
            
        sim_list.sort(reverse=True)
        return sim_list
        

    def get_similar_items_from_model(self, item, user_list, model, min_value=MIN_SIMILARITY_VALUE):
        user_item_matrix = self.create_matrix_from_model(user_list, model)
        item_user_matrix = self.rotate_matrix(user_item_matrix)
#	assert False, (user_item_matrix, item_user_matrix)
        sim_list = []
	item_list=model.objects.all()
        for other in item_list:
            if item==other:continue
#	    assert False, item_user_matrix[item.id]
#            sim=utils.distance_matrix_p1_p2(item_user_matrix[item.id],item_user_matrix[other.id]) #returns a 0..1 value
            sim=utils.distance_matrix_p1_p2(item_user_matrix.get(item.id,
			{1:Vote()}),
		item_user_matrix.get(other.id, 
			{1:Vote()}))
	    """
            sim=utils.distance_matrix_p1_p2(item_user_matrix.get(item.id,
			{1:Vote(	object=item,
				object_id=item.id,
				user=user_list[0],
				vote=0,
				content_type=ContentType.objects.get_for_model(item)
			)}),
		item_user_matrix.get(other.id, 
			{1:Vote(	object=item,
				object_id=item.id,
				user=user_list[0],
				vote=0,
				content_type=ContentType.objects.get_for_model(item)
			)}
		)) #returns a 0..1 value
	    """
            if sim>min_value:
                sim_list.append((sim,other))

        assert False, sim_list            
        sim_list.sort(reverse=True)
        return sim_list
        

    def create_matrix(self, users, items):
        user_item_matrix = {}
        for user in users:
            votes_for_user = Vote.objects.get_for_user_in_bulk(items, user)
            user_item_matrix[user.id] = votes_for_user
        
        return user_item_matrix
    
    def create_matrix_from_model(self, users, model):
        user_item_matrix = {}
        for user in users:
            votes_for_user = Vote.objects.get_for_user_from_model(model, user)
            user_item_matrix[user.id] = votes_for_user
        
        return user_item_matrix

    def rotate_matrix(self, matrix):
        rotated_matrix = {}
        for user in matrix:
            for item in matrix[user]:
                rotated_matrix.setdefault(item,{})
                rotated_matrix[item][user]=matrix[user][item]
        return rotated_matrix
        
# Content Based Recommendations
    def get_content_based_recs(self, user, tagged_items, min_value=MIN_CONTENT_BASED_RECOMMENDATION_VALUE):
        ''' For a given user tags and a dicc of item tags, returns the distances between the user and the items
            >>> eng=RecommenderManager()
            >>> user_tags=['a','b','c','d']
            >>> tag_matrix={}
            >>> tag_matrix['it1']=['z','a','c']
            >>> tag_matrix['it2']=['b','c']
            >>> tag_matrix['it3']=['a','r','t','v']
            >>> eng.get_content_based_recs(user_tags,tag_matrix)
            [(7.5, 'it1'), (10.0, 'it2'), (5.0, 'it3')]
        '''

        item_tag_matrix = {}
        for item in tagged_items:
            item_tag_matrix[item] = Tag.objects.get_for_object(item)
        
        user_tags = Tag.objects.get_for_object(user)

        recs = []
        for item,item_tags in item_tag_matrix.items():
            sim = utils.tanamoto2(item_tags, user_tags)
            if sim>min_value:
                recs.append((sim, item))
                
        return recs


    def get_by_relevance_to_tags(self, search_tags, tagged_items, min_value=MIN_CONTENT_BASED_RECOMMENDATION_VALUE):
        ''' For a given user tags and a dicc of item tags, returns the distances between the user and the items
            >>> eng=RecommenderManager()
            >>> user_tags=['a','b','c','d']
            >>> tag_matrix={}
            >>> tag_matrix['it1']=['z','a','c']
            >>> tag_matrix['it2']=['b','c']
            >>> tag_matrix['it3']=['a','r','t','v']
            >>> eng.get_content_based_recs(user_tags,tag_matrix)
            [(7.5, 'it1'), (10.0, 'it2'), (5.0, 'it3')]
        '''

        item_tag_matrix = {}
        for item in tagged_items:
            item_tag_matrix[item] = Tag.objects.get_for_object(item)
        
        recs = []
        for item,item_tags in item_tag_matrix.items():
            sim = utils.tanamoto2([str(tg) for tg in item_tags], [str(tg) for tg in search_tags])
            if sim>min_value:
                recs.append((sim, item))
                
        return recs
    
       
# Clustering methods
    def cluster_users(self, users, items, cluster_count=2):
        user_item_matrix = self.create_matrix(users, items)
        return utils.kcluster(user_item_matrix, items, cluster_count)

    def cluster_items(self, users, items, cluster_count=2):
        user_item_matrix = self.create_matrix(users, items)
        item_user_matrix = self.rotate_matrix(user_item_matrix)
        return utils.kcluster(item_user_matrix, users, cluster_count)


# Home-made methods
    def get_votearray_for_user(self, user):
        """Return a list of all of the values (1,0,-1) on all votes objects of objectType"""
        votearray = user.usermeta.all()[0].votearray
        return votearray

    def userSim(self, user1, user2):
        """Get the simmilarity in votes between 2 users (between 0 and 1)"""
        va1 = self.get_votearray_for_user(user1)
        va2 = self.get_votearray_for_user(user2)
        sim = utils.pearson_correlation(va1,va2)
        return sim

    def get_mean_vote_for_user(self, user):
        mean = user.usermeta.all()[0].meanvote
        return mean

    def get_pred_vote_for_user_on_item(self, user, item):
        """Does the following equation
        
        $\\bar{r}_u + \\frac{\sum_{n \subset neighbours(u)}{usersim(u,n)\mul(r_{ni}-\\bar{r}_n)}}{\sum_{n \subset neighbours(u)}{usersim(u,n)}}$
        
        to get the predicted vote of a user on an item
        """
        objectType = type(item)
        mean_user_vote = self.get_mean_vote_for_user(user) #rbar_u
        neighbours = User.objects.exclude(id=user.id)

        sum_sim = sum([self.userSim(neighbour, user) for neighbour in neighbours])	#bottom frac
        sum_votes = sum([(self.userSim(neighbour, user)*							#top frac
            (Vote.objects.get_val_for_user(item, user)-self.get_mean_vote_for_user(neighbour) ) )
            for neighbour in neighbours])
        value = mean_user_vote+(sum_votes/sum_sim)

        return value

    def get_pred_votes_for_user_on_items(self, user, items):
#        poke("total","none")
        try:
            iter(items) #try and treat the object as a sequence
        except:
            items = [items] #we were passed a single item, stick in in a list

        objectType = type(items[0])
        mean_user_vote = self.get_mean_vote_for_user(user) #rbar_u
        neighbours = User.objects.exclude(id=user.id)

        sum_sim = 0 #bottom frac
        sims = {} #store similarities in dict to save recomputing them
        for neighbour in neighbours:
            sim = self.userSim(neighbour, user)
            sims[neighbour.id] = sim

            sum_sim += sim #accumulate the sum of similarities (bottom of frac)

        return_list = []
        for item in items:
#            poke("iter", "None")
            sum_votes = sum([(sims[neighbour.id]*							#top frac
                (Vote.objects.get_val_for_user(item, user)-self.get_mean_vote_for_user(neighbour) ) )
                for neighbour in neighbours])
            value = mean_user_vote+(sum_votes/float(sum_sim+0.0001))
            return_list.append((value,item))
#            poke("iter", "post")

#        poke("total","done")
#        output()
        return sorted(return_list, reverse=True)

    def get_recommendations_for_user_on_items(self, user, items, number=False):
        if number:
            return sorted(self.get_pred_votes_for_user_on_items(user, items), reverse=True)[:number]
        else:
            return sorted(self.get_pred_votes_for_user_on_items(user, items), reverse=True)













