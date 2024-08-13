import os

import numpy as np


class BasicMatrixFactorizationRecommender:
    def __init__(self):
        my_path = os.path.dirname(__file__)
        self.W = np.load(my_path + '/W.npy')
        self.U = np.load(my_path + '/U.npy')
        self.b = np.load(my_path + '/b.npy')
        self.c = np.load(my_path + '/c.npy')
        self.mu = np.load(my_path + '/mu.npy')

    def predict(self, user_id, movie_id):
        # Calculate the predicted rating
        user_id = int(user_id)
        movie_id = int(movie_id)

        if not (0 <= user_id < self.W.shape[0]):
            raise ValueError(f"user_id {user_id} is out of bounds")
        if not (0 <= movie_id < self.U.shape[0]):
            raise ValueError(f"movie_id {movie_id} is out of bounds")

        predicted_rating = self.W[user_id].dot(self.U[movie_id]) + self.b[user_id] + self.c[movie_id] + self.mu
        return predicted_rating
