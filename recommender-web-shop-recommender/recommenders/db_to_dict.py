from dao import UserMovieRatingDao


user_movie_rating_dao = UserMovieRatingDao()
user2movie = user_movie_rating_dao.get_user_movies()
movie2user = user_movie_rating_dao.get_movie_users()
usermovie2rating = user_movie_rating_dao.get_user_movie_rating()

pickle_util = PickleUtil()
pickle_util.dump_binary_dict('user2movie.bin', user2movie)
pickle_util.dump_binary_dict('movie2user.bin', movie2user)
pickle_util.dump_binary_dict('usermovie2rating.bin', usermovie2rating)
#pickle_util.dump_binary_dict('usermovie2rating_test.bin', usermovie2rating_test)
