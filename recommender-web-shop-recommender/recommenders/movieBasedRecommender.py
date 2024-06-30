import os
import pickle

import numpy as np
from sortedcontainers import SortedList


def predict(user, movie):
    nominator = 0
    denominator = 0

    for neg_w, other_movie in neighbours[movie]:
        try:
            nominator += -neg_w * deviations[other_movie][user]
            denominator += abs(neg_w)
        except KeyError:
            pass

    if denominator == 0:
        prediction = averages[movie]
    else:
        prediction = averages[movie] + nominator / denominator

    prediction = min(5, prediction)
    prediction = max(0.5, prediction)
    return prediction


def mean_squared_error(p, t):
    p = np.array(p)
    t = np.array(t)

    return np.mean((p - t) ** 2)


if __name__ == '__main__':

    if not os.path.exists('user2movie.bin') or \
            not os.path.exists('movie2user.bin') or \
            not os.path.exists('usermovie2rating.bin') or \
            not os.path.exists('usermovie2rating_test.bin'):
        pass

    user2movie = {}
    movie2user = {}
    usermovie2rating = {}
    usermovie2rating_test = {}

    with (open('user2movie.bin', 'rb')) as f:
        user2movie = pickle.load(f)

    with (open('movie2user.bin', 'rb')) as f:
        movie2user = pickle.load(f)

    with (open('usermovie2rating.bin', 'rb')) as f:
        usermovie2rating = pickle.load(f)

    with (open('usermovie2rating_test.bin', 'rb')) as f:
        usermovie2rating_test = pickle.load(f)

    movie_count = np.max(list(movie2user.keys())) + 1
    u1 = np.max(list(user2movie.keys()))
    u2 = np.max([u for (u, m), r in usermovie2rating_test.items()])
    user_count = max(u1, u2)

    K = 20
    limit = 5
    neighbours = {}
    averages = []
    deviations = []
    for i in range(movie_count):

        users_i = movie2user[i]
        users_i_set = set(users_i)
        ratings_i = {user: usermovie2rating[user, i] for user in users_i}
        avg_i = np.mean(list(ratings_i.values()))

        dev_i = {user: (rating - avg_i) for user, rating in ratings_i.items()}
        dev_i_values = np.array(list(dev_i.values()))
        sigma_i = np.sqrt(dev_i_values.dot(dev_i_values))

        deviations.append(dev_i)
        averages.append(avg_i)
        sorted_list = SortedList()

        for j in range(movie_count):
            if i == j:
                continue

            users_j = movie2user[j]
            users_j_set = set(users_j)
            users_in_common = users_i_set.intersection(users_j_set)

            if len(users_in_common) > limit:
                ratings_j = {user: usermovie2rating[user, j] for user in users_j}
                avg_j = np.mean(list(ratings_j.values()))

                dev_j = {user: (rating - avg_j) for user, rating in ratings_j.items()}
                dev_j_values = np.array(list(dev_j.values()))
                sigma_j = np.sqrt(dev_j_values.dot(dev_j_values))

                numerator = sum(dev_i[u] * dev_j[u] for u in users_in_common)
                w_ij = numerator / (sigma_i * sigma_j)

                sorted_list.add((-w_ij, j))

                if len(sorted_list) > K:
                    del sorted_list[-1]

        neighbours[i] = sorted_list
        print(f"On movie: {i}/{movie_count}")

    training_predictions = []
    training_targets = []

    test_predictions = []
    test_targets = []

    for (u, m), rating in usermovie2rating.items():
        training_predictions.append(predict(u, m))
        training_targets.append(rating)

    for (u, m), rating in usermovie2rating_test.items():
        test_predictions.append(predict(u, m))
        test_targets.append(rating)

    print(f"MSE train: {mean_squared_error(training_predictions, training_targets)}")
    print(f"MSE test: {mean_squared_error(test_predictions, test_targets)}")
