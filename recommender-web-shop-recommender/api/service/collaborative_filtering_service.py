from ...recommenders.collaborative_filtering import CollaborativeFiltering
from ...dao.user_movie_rating_dao import UserMovieRatingDao
from sortedcontainers import SortedList
from operator import neg

class CollaborativeFilteringService:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(CollaborativeFilteringService, cls).__new__(cls, *args, **kwargs)
        return cls._instance
    
    def __init__(self):
         self.umr_dao = UserMovieRatingDao()
         self.cf = CollaborativeFiltering()

    # def get_user_user_top_n(self, user_id, n):
    #     rated_movies = self.umr_dao.get_rated_movies_excluding_user(user_id)
        # self.cf.predict(u, m)

    def get_movie_movie_top_n(self, user_id, n):
        rated_movies = self.umr_dao.get_rated_movies_excluding_user(user_id)
        top_five_rating = SortedList(key=neg)

        for movie_id in rated_movies:
           top_five_rating.add((self.cf.predict(movie_id, user_id)), movie_id)

           if len(top_five_rating > n):
               del top_five_rating[-1]

        return top_five_rating