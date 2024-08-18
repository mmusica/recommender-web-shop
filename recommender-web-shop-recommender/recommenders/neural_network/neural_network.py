#code modified from https://github.com/lazyprogrammer/machine_learning_examples/blob/master/recommenders/mf_keras_deep.py

from __future__ import print_function, division
from dao.user_movie_rating_dao import UserMovieRatingDao

import numpy as np
import matplotlib.pyplot as plt

from keras.api.models import Model
from keras.api.layers import Input, Embedding, Flatten, Dense, Concatenate
from keras.api.layers import Activation

dao = UserMovieRatingDao()

usermovie2rating, usermovie2rating_test, user2movie, movie2user = (
    dao.get_train_and_test_set()
)

mu = np.mean(list(usermovie2rating.values()))

train_user_ids = np.array([user for (user, movie) in usermovie2rating.keys()])
train_movie_ids = np.array([movie for (user, movie) in usermovie2rating.keys()])
train_ratings = np.array(list(usermovie2rating.values())) - mu

test_user_ids = np.array([user for (user, movie) in usermovie2rating_test.keys()])
test_movie_ids = np.array([movie for (user, movie) in usermovie2rating_test.keys()])
test_ratings = np.array(list(usermovie2rating_test.values())) - mu

N = np.max(list(user2movie.keys())) + 1
m1 = np.max(list(movie2user.keys()))
m2 = np.max([m for (u, m), r in usermovie2rating_test.items()])
M = max(m1, m2) + 1

K = 10
epochs = 15


u = Input(shape=(1,))
m = Input(shape=(1,))
u_embedding = Embedding(N, K)(u)  # (N, 1, K)
m_embedding = Embedding(M, K)(m)  # (N, 1, K)
u_embedding = Flatten()(u_embedding)  # (N, K)
m_embedding = Flatten()(m_embedding)  # (N, K)
x = Concatenate()([u_embedding, m_embedding])  # (N, 2K)

x = Dense(400)(x)
x = Activation('relu')(x)
x = Dense(1)(x)

model = Model(inputs=[u, m], outputs=x)
model.compile(
    loss='mse',
    optimizer='adam',
    metrics=['mse'],
)

r = model.fit(
    x=[train_user_ids, train_movie_ids],
    y=train_ratings,
    epochs=epochs,
    batch_size=128,
    validation_data=(
        [test_user_ids, test_movie_ids],
        test_ratings
    ),
    verbose=2,
)

plt.plot(r.history['mse'], label="trening mse")
plt.plot(r.history['val_mse'], label="testni mse")
plt.legend()
plt.show()

model.save('movie_recommender_model.keras')
np.save('mu.npy', mu)
