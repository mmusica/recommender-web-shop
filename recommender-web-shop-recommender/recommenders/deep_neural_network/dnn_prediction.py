import os

import numpy as np
from keras.api.models import load_model


class DeepNeuralNetwork:
    def __init__(self):
        my_path = os.path.dirname(__file__)
        self.mu = np.load(my_path + '/mu.npy')
        self.model = load_model(my_path + "/movie_recommender_model.keras")

    def predict(self, user_id, movie_id):
        user_id = np.array(user_id).reshape(1, 1)
        movie_id = np.array(movie_id).reshape(1, 1)

        predicted_rating = self.model.predict([user_id, movie_id])
        predicted_rating += self.mu

        return predicted_rating[0][0]

    def predict_batch(self, user_id, movie_batch):
        user_id_array = np.array([user_id] * len(movie_batch)).reshape(-1, 1)
        movie_id_array = np.array(movie_batch).reshape(-1, 1)

        predicted_ratings = self.model.predict([user_id_array, movie_id_array]).flatten()
        predicted_ratings += self.mu
        return predicted_ratings
