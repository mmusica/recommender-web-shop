from sortedcontainers import SortedList
from recommenders.matrix_factorization import BasicMatrixFactorizationRecommender
from dao import UserMovieRatingDao


class MatrixFactorizationService:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(MatrixFactorizationService, cls).__new__(cls, *args, **kwargs)
        return cls._instance


    def __init__(self):
        self.umr_dao = UserMovieRatingDao()
        self.bmfr = BasicMatrixFactorizationRecommender()

    def get_top_n_movies_for_user_bmfr(self, user_id, n):
        rated_movies = self.umr_dao.get_rated_movies_excluding_user(user_id)
        top_five_rating = SortedList(key=lambda x: -x[0])

        for movie_id in rated_movies:
            predicted_rating = self.bmfr.predict(user_id, movie_id)
            top_five_rating.add((predicted_rating, movie_id))

            if len(top_five_rating) > int(n):
                del top_five_rating[-1]

        return [{"movieId": m, "rating": r} for r, m in top_five_rating]