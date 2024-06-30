import pickle

import pandas as pd
from sklearn.utils import shuffle

count = 0


def update_user2movie_and_movie2user(row):
    global count
    count += 1
    if count % 100_000 == 0:
        print("Processed %.3f" % (float(count / cutoff)))

    user_id = int(row.userId)
    movie_id = int(row.movie_indx)

    if user_id not in user2movie:
        user2movie[user_id] = [movie_id]
    else:
        user2movie[user_id].append(movie_id)

    if movie_id not in movie2user:
        movie2user[movie_id] = [user_id]
    else:
        movie2user[movie_id].append(user_id)

    usermovie2rating[(user_id, movie_id)] = row.rating


def update_usermoveie2rating_test(row):
    user_id = int(row.userId)
    movie_id = int(row.movie_indx)

    usermovie2rating_test[(user_id, movie_id)] = row.rating


df = pd.read_csv('../large_files/movielens-20m-dataset/small_rating.csv')

num_of_users = df.userId.max() + 1
num_of_movies = df.movie_indx.max() + 1

df = shuffle(df)
cutoff = int(0.8 * len(df))

df_train = df[:cutoff]
df_test = df[cutoff:]

user2movie = {}
movie2user = {}
usermovie2rating = {}
usermovie2rating_test = {}

df_train.apply(lambda row: update_user2movie_and_movie2user(row), axis='columns')
df_test.apply(lambda row: update_usermoveie2rating_test(row), axis='columns')

with (open('user2movie.bin', 'wb')) as f:
    pickle.dump(user2movie, f)

with (open('movie2user.bin', 'wb')) as f:
    pickle.dump(movie2user, f)

with (open('usermovie2rating_test.bin', 'wb')) as f:
    pickle.dump(usermovie2rating_test, f)

with (open('usermovie2rating.bin', 'wb')) as f:
    pickle.dump(usermovie2rating, f)
