from typing import Dict
import numpy as np
from sortedcontainers import SortedList
from utils import PickleUtil
import os


class CollaborativeFiltering:
    def __init__(
        self,
        user2movie: Dict = None,
        movie2user: Dict = None,
        usermovie2rating: Dict = None,
    ):
        self.deviations = None
        self.averages = None
        self.neighbours = None
        self.user2movie = user2movie
        self.movie2user = movie2user
        self.usermovie2rating = usermovie2rating
        self.my_path = os.path.dirname(__file__)

    def reset(self):
        self.__init__()

    def mean_squared_error(self, p, t):
        p = np.array(p)
        t = np.array(t)

        return np.mean((p - t) ** 2)

    def predict(self, entity_to_predict, entity_predicting_with, type):
        utils = PickleUtil()
        if type == "movie" and self.averages is None:
            self.averages = utils.load_binary_dict(self.my_path + "/averages_movie.bin")
            self.deviations = utils.load_binary_dict(
                self.my_path + "/deviations_movie.bin"
            )
            self.neighbours = utils.load_binary_dict(
                self.my_path + "/neighbours_movie.bin"
            )

        if type == "user" and self.averages is None:
            self.averages = utils.load_binary_dict(self.my_path + "/averages_user.bin")
            self.deviations = utils.load_binary_dict(
                self.my_path + "/deviations_user.bin"
            )
            self.neighbours = utils.load_binary_dict(
                self.my_path + "/neighbours_user.bin"
            )

        numerator = 0
        denominator = 0

        for neg_w, other_entity in self.neighbours[entity_to_predict]:
            try:
                numerator += (
                    -neg_w * self.deviations[other_entity][entity_predicting_with]
                )
                denominator += abs(neg_w)
            except KeyError:
                pass

        if denominator == 0:
            prediction = self.averages[entity_to_predict]
        else:
            prediction = self.averages[entity_to_predict] + numerator / denominator

        prediction = min(5, prediction)
        prediction = max(0.5, prediction)  # min rating is 0.5
        return prediction

    def __calculate_sigma(self, dev):
        dev_values = np.array(list(dev.values()))
        return np.sqrt(dev_values.dot(dev_values))

    def __calculate_values(self, dev, ratings, i):
        avg = np.mean(list(ratings.values()))
        new_dev = {user: (rating - avg) for user, rating in ratings.items()}
        # appends the deviations of user ratings for each  item (i)
        dev.update(new_dev)
        # appends averages and deviations
        self.deviations[i] = dev
        self.averages[i] = avg

    def user_user_calculate(self, movies, dev, user_id):
        # get ratings of every movie for this specific user
        ratings = {movie: self.usermovie2rating[(user_id, movie)] for movie in movies}
        self.__calculate_values(dev, ratings, user_id)

    def movie_calculate_values(self, users, dev, movie_index):
        # get ratings that each user has for this specific movie
        ratings = {user: self.usermovie2rating[(user, movie_index)] for user in users}
        self.__calculate_values(dev, ratings, movie_index)

    def __dump(self, neighbours_f, averages_f, deviations_f):
        pk = PickleUtil()
        pk.dump_binary_dict(self.my_path + neighbours_f, self.neighbours)
        pk.dump_binary_dict(self.my_path + averages_f, self.averages)
        pk.dump_binary_dict(self.my_path + deviations_f, self.deviations)
        self.reset()

    def movie_movie_based(self, K, limit):
        self.neighbours = {}
        self.averages = {}
        self.deviations = {}

        count = 0

        for i in self.movie2user.keys():
            users_i = self.movie2user[i]
            users_i_set = set(users_i)
            dev_i = {}
            self.movie_calculate_values(users_i, dev_i, i)
            sigma_i = self.__calculate_sigma(dev_i)

            sorted_list = SortedList()

            for j in self.movie2user.keys():
                if i == j:
                    continue

                users_j = self.movie2user[j]
                users_j_set = set(users_j)
                users_in_common = users_i_set.intersection(users_j_set)

                if len(users_in_common) > limit:
                    dev_j = {}
                    self.movie_calculate_values(users_j, dev_j, j)
                    sigma_j = self.__calculate_sigma(dev_j)

                    numerator = sum(dev_i[u] * dev_j[u] for u in users_in_common)
                    w_ij = numerator / (sigma_i * sigma_j)

                    sorted_list.add((-w_ij, j))

                    if len(sorted_list) > K:
                        del sorted_list[-1]

            self.neighbours[i] = sorted_list
            print(f"On movie: {count}/{len(self.movie2user.keys())}")
            count += 1

        self.__dump(
            "/neighbours_movie.bin", "/averages_movie.bin", "/deviations_movie.bin"
        )

    def user_user_based(self, K, limit):
        self.neighbours = {}
        self.averages = {}
        self.deviations = {}

        user_count = np.max(list(self.user2movie.keys())) + 1
        count = 0
        for i in self.user2movie.keys():
            movies_i = self.user2movie[i]
            movies_i_set = set(movies_i)

            dev_i = {}
            self.user_user_calculate(movies_i, dev_i, i)
            sigma_i = self.__calculate_sigma(dev_i)

            sorted_list = SortedList()

            for j in self.user2movie.keys():
                if j == i:
                    continue

                movies_j = self.user2movie[j]
                movies_j_set = set(movies_j)
                common_movies = movies_i_set.intersection(movies_j_set)

                if len(common_movies) > limit:
                    dev_j = {}
                    self.user_user_calculate(movies_j, dev_j, j)
                    sigma_j = self.__calculate_sigma(dev_j)

                    numerator = sum(dev_i[m] * dev_j[m] for m in common_movies)
                    w_ij = numerator / (sigma_i * sigma_j)

                    sorted_list.add((-w_ij, j))

                    if len(sorted_list) > K:
                        del sorted_list[-1]

            self.neighbours[i] = sorted_list
            print(f"On user: {count}/{user_count}")
            count += 1

        self.__dump("/neighbours_user.bin", "/averages_user.bin", "/deviations_user.bin")
