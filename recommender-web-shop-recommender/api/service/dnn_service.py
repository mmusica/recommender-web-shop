import numpy as np
from sortedcontainers import SortedList

from recommenders.neural_network.dnn_prediction import NeuralNetwork

from dao import UserMovieRatingDao


class DNNService:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(DNNService, cls).__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self):
        self.umr_dao = UserMovieRatingDao()
        self.dnn = NeuralNetwork()

    def get_top_n_movies_for_user(self, user_id, n):
        user_id = int(user_id)
        n = int(n)
        rated_movies = self.umr_dao.get_rated_movies_excluding_user(user_id)
        top_five_rating = SortedList(key=lambda x: -x[0])

        for movie_id in rated_movies:
            predicted_rating = self.dnn.predict(user_id, movie_id)
            top_five_rating.add((predicted_rating, movie_id))

            if len(top_five_rating) > int(n):
                del top_five_rating[-1]

        return [{"movieId": m, "rating": float(r)} for r, m in top_five_rating]

    def get_top_n_movie_for_user_batch(self, user_id, n):
        user_id = int(user_id)
        n = int(n)
        movie_batch = self.umr_dao.get_rated_movies_excluding_user(user_id)
        predicted_ratings = self.dnn.predict_batch(user_id, movie_batch)

        top_n_ratings = sorted(zip(predicted_ratings, movie_batch), reverse=True)[:n]
        return [{"movieId": m, "rating": float(r)} for r, m in top_n_ratings]