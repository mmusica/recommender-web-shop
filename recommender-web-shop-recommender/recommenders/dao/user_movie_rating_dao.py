import psycopg2
from sklearn.utils import shuffle

USER_ID = 1
MOVIE_ID = 2
RATING = 3


class UserMovieRatingDao:

    def __init__(self):
        self.train_user2movie = {}
        self.train_movie2user = {}

    def __get_connection(self):
        return psycopg2.connect(database='recommender-web-shop', user='mmusica', password='pass', host='localhost',
                                port='5432')

    def __close_connection(self, conn, cur):
        conn.commit()
        cur.close()
        conn.close()

    def get_user_movies(self):
        conn = self.__get_connection()
        sql = """SELECT * FROM user_movie_rating"""
        cur = conn.cursor()
        cur.execute(sql)
        row = cur.fetchone()

        user2movie = {}
        while row:
            if row[USER_ID] not in user2movie:
                user2movie[row[USER_ID]] = [row[MOVIE_ID]]
            else:
                user2movie[row[USER_ID]].append(row[MOVIE_ID])

            row = cur.fetchone()
        self.__close_connection(conn, cur)
        return user2movie

    def get_movie_users(self):
        conn = self.__get_connection()
        sql = """SELECT * FROM user_movie_rating"""
        cur = conn.cursor()
        cur.execute(sql)
        row = cur.fetchone()

        movie2user = {}
        while row:
            if row[MOVIE_ID] not in movie2user:
                movie2user[row[MOVIE_ID]] = [row[USER_ID]]
            else:
                movie2user[row[MOVIE_ID]].append(row[USER_ID])

            row = cur.fetchone()
        self.__close_connection(conn, cur)
        return movie2user

    def get_user_movie_rating(self):
        conn = self.__get_connection()
        sql = """SELECT * FROM user_movie_rating"""
        cur = conn.cursor()
        cur.execute(sql)
        row = cur.fetchone()

        usermovie2rating = {}
        while row:
            key = (row[USER_ID], row[MOVIE_ID])
            value = row[RATING]
            usermovie2rating[key] = value
            row = cur.fetchone()

        self.__close_connection(conn, cur)
        return usermovie2rating

    def get_train_and_test_set(self):
        """
        Gets every rating from database and then creates train and test sets

        Returns
        -------
        dict, dict, dict, dict
            Four dictionaries: first for the training set and second for the test set,
            two mapping user-movie pairs to ratings.
            Third and fourth dictionaries are user2movie and movie2user of said train set.
        """

        conn = self.__get_connection()
        sql = """SELECT * FROM user_movie_rating"""
        cur = conn.cursor()
        cur.execute(sql)
        all_ratings = cur.fetchall()
        all_ratings = shuffle(all_ratings)

        cutoff = int(0.8 * len(all_ratings))

        all_train = all_ratings[:cutoff]
        all_test = all_ratings[cutoff:]

        usermovie2rating_test = {}
        usermovie2rating = {}

        for row in all_train:
            key = (row[USER_ID], row[MOVIE_ID])
            value = row[RATING]
            usermovie2rating[key] = value

            if row[MOVIE_ID] not in self.train_movie2user:
                self.train_movie2user[row[MOVIE_ID]] = [row[USER_ID]]
            else:
                self.train_movie2user[row[MOVIE_ID]].append(row[USER_ID])

            if row[USER_ID] not in self.train_user2movie:
                self.train_user2movie[row[USER_ID]] = [row[MOVIE_ID]]
            else:
                self.train_user2movie[row[USER_ID]].append(row[MOVIE_ID])

        for row in all_test:
            key = (row[USER_ID], row[MOVIE_ID])
            value = row[RATING]
            usermovie2rating_test[key] = value

        self.__close_connection(conn, cur)
        return usermovie2rating, usermovie2rating_test, self.train_user2movie, self.train_movie2user


if __name__ == '__main__':
    user_dao = UserMovieRatingDao()
    user_movies = user_dao.get_user_movies()
    print(len(user_movies[1]))

    movie_users = user_dao.get_movie_users()
    # print(movie_users[1])

    rating = user_dao.get_user_movie_rating()
    print(rating[(2, 3)])
