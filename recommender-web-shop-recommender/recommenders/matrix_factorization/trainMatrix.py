from dao.user_movie_rating_dao import UserMovieRatingDao
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime

if __name__ == '__main__':
    dao = UserMovieRatingDao()

    usermovie2rating, usermovie2rating_test, user2movie, movie2user = (
        dao.get_train_and_test_set()
    )
    N = np.max(list(user2movie.keys())) + 1
    # the test set may contain movies the train set doesn't have data on
    m1 = np.max(list(movie2user.keys()))
    m2 = np.max([m for (u, m), r in usermovie2rating_test.items()])
    M = max(m1, m2) + 1
    print("N:", N, "M:", M)


    # initialize variables
    K = 10 # latent dimensionality #Faktori su tu skriveni ali matrica ih uci, npr akcija komedija itd.
    W = np.random.randn(N, K)
    b = np.zeros(N)
    U = np.random.randn(M, K)
    c = np.zeros(M)
    mu = np.mean(list(usermovie2rating.values()))

    # prediction[i,j] = W[i].dot(U[j]) + b[i] + c.T[j] + mu

    def get_loss(d):
        # d: (user_id, movie_id) -> rating
        N = float(len(d))
        sse = 0
        for k, r in d.items():
            i, j = k
            p = W[i].dot(U[j]) + b[i] + c[j] + mu
            sse += (p - r)*(p - r)
        return sse / N


    # train the parameters
    epochs = 25
    reg = 20.   # regularization penalty
    train_losses = []
    test_losses = []
    for epoch in range(epochs):
        print("epoch:", epoch)
        epoch_start = datetime.now()
        # perform updates

        # update W and b
        t0 = datetime.now()
        for i in user2movie.keys():
            # for W
            matrix = np.eye(K) * reg
            vector = np.zeros(K)

            # for b
            bi = 0
            for j in user2movie[i]:
                r = usermovie2rating[(i, j)]
                matrix += np.outer(U[j], U[j])
                vector += (r - b[i] - c[j] - mu)*U[j]
                bi += (r - W[i].dot(U[j]) - c[j] - mu)

            # set the updates
            W[i] = np.linalg.solve(matrix, vector)
            b[i] = bi / (len(user2movie[i]) + reg)

            if i % (N//10) == 0:
                print("i:", i, "N:", N)
        print("updated W and b:", datetime.now() - t0)

        # update U and c
        t0 = datetime.now()
        for j in movie2user.keys():
            # for U
            matrix = np.eye(K) * reg
            vector = np.zeros(K)

            # for c
            cj = 0
            try:
                for i in movie2user[j]:
                    r = usermovie2rating[(i,j)]
                    matrix += np.outer(W[i], W[i])
                    vector += (r - b[i] - c[j] - mu)*W[i]
                    cj += (r - W[i].dot(U[j]) - b[i] - mu)

                # set the updates
                U[j] = np.linalg.solve(matrix, vector)
                c[j] = cj / (len(movie2user[j]) + reg)

                if j % (M//10) == 0:
                    print("j:", j, "M:", M)
            except KeyError:
                # possible not to have any ratings for a movie
                pass
        print("updated U and c:", datetime.now() - t0)
        print("epoch duration:", datetime.now() - epoch_start)


        # store train loss
        t0 = datetime.now()
        train_losses.append(get_loss(usermovie2rating))

        # store test loss
        test_losses.append(get_loss(usermovie2rating_test))
        print("calculate cost:", datetime.now() - t0)
        print("train loss:", train_losses[-1])
        print("test loss:", test_losses[-1])


    print("train losses:", train_losses)
    print("test losses:", test_losses)

    # plot losses
    plt.plot(train_losses, label="train loss")
    plt.plot(test_losses, label="test loss")
    plt.legend()
    plt.show()

    np.save('W.npy', W)
    np.save('U.npy', U)
    np.save('b.npy', b)
    np.save('c.npy', c)
    np.save('mu.npy', mu)