import os
import pickle

import numpy as np
from sortedcontainers import SortedList


def predict(user, movie):
    numerator = 0
    denominator = 0

    for neg_w, other_user in neighbors[user]:
        try:
            numerator += -neg_w * deviations[other_user][movie]
            denominator += abs(neg_w)
        except KeyError:
            pass

    if denominator == 0:
        prediction = averages[user]
    else:
        prediction = averages[user] + numerator / denominator

    prediction = min(5, prediction)
    prediction = max(0.5, prediction)  # max rating is 0.5
    return prediction


def mean_squared_error(p, t):
    p = np.array(p)
    t = np.array(t)

    return np.mean((p - t) ** 2)


if __name__ == '__main__':
    if not os.path.exists('user2movie.bin') or \
            not os.path.exists('movie2user.bin') or \
            not os.path.exists('usermovie2rating_test.bin') or \
            not os.path.exists('usermovie2rating.bin'):
        print("bin files missing, starting generation...")

    with (open('movie2user.bin', 'rb')) as f:
        movie2user = pickle.load(f)

    with (open('user2movie.bin', 'rb')) as f:
        user2movie = pickle.load(f)

    with (open('usermovie2rating.bin', 'rb')) as f:
        usermovie2rating = pickle.load(f)

    with (open('usermovie2rating_test.bin', 'rb')) as f:
        usermovie2rating_test = pickle.load(f)

    user_count = np.max(list(user2movie.keys())) + 1

    m1 = np.max(list(movie2user.keys()))
    m2 = np.max([m for (u, m), r in usermovie2rating_test.items()])
    movie_count = max(m1, m2) + 1

    K = 25
    limit = 5
    neighbors = {}
    averages = []
    deviations = []

    for i in range(user_count):
        movies_i = user2movie[i]
        movies_i_set = set(movies_i)

        ratings_i = {movie: usermovie2rating[(i, movie)] for movie in movies_i}
        avg_i = np.mean(list(ratings_i.values()))
        dev_i = {movie: (rating - avg_i) for movie, rating in ratings_i.items()}
        devi_i_values = np.array(list(dev_i.values()))
        sigma_i = np.sqrt(devi_i_values.dot(devi_i_values))

        averages.append(avg_i)
        deviations.append(dev_i)

        sorted_list = SortedList()

        for j in range(user_count):
            if j == i:
                continue

            movies_j = user2movie[j]
            movies_j_set = set(movies_j)
            common_movies = movies_i_set.intersection(movies_j_set)

            if len(common_movies) > limit:
                ratings_j = {movie: usermovie2rating[(j, movie)] for movie in movies_j}
                avg_j = np.mean(list(ratings_j.values()))
                dev_j = {movie: (rating - avg_j) for movie, rating in ratings_j.items()}
                dev_j_values = np.array(list(dev_j.values()))
                sigma_j = np.sqrt(dev_j_values.dot(dev_j_values))

                numerator = sum(dev_i[m] * dev_j[m] for m in common_movies)
                w_ij = numerator / (sigma_i * sigma_j)

                sorted_list.add((-w_ij, j))

                if len(sorted_list) > K:
                    del sorted_list[-1]

        neighbors[i] = sorted_list
        print(f"On user: {i}/{user_count}")

    train_predictions = []
    train_targets = []

    test_predictions = []
    test_targets = []

    for (user, movie), rating in usermovie2rating.items():
        train_predictions.append(predict(user, movie))
        train_targets.append(rating)

    for (user, movie), rating in usermovie2rating_test.items():
        test_predictions.append(predict(user, movie))
        test_targets.append(rating)

    print(f"MSE train: {mean_squared_error(train_predictions, train_targets)}")
    print(f"MSE test: {mean_squared_error(test_predictions, test_targets)}")
