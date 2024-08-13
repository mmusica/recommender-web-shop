from collaborative_filtering import CollaborativeFiltering
from dao.user_movie_rating_dao import UserMovieRatingDao

if __name__ == "__main__":
    dao = UserMovieRatingDao()
  

    usermovie2rating, usermovie2rating_test, user2movie, movie2user = (
        dao.get_train_and_test_set()
    )
    cf = CollaborativeFiltering(
        user2movie, movie2user, usermovie2rating 
    )

    cf.user_user_based(25, 5)
    # cf = CollaborativeFiltering()

    training_predictions = []
    training_targets = []

    test_predictions = []
    test_targets = []

   
    # for (u, m), rating in usermovie2rating.items():
    #     training_predictions.append(cf.predict(m, u, "movie"))
    #     training_targets.append(rating)
    #
    # for (u, m), rating in usermovie2rating_test.items():
    #     test_predictions.append(cf.predict(m, u, "movie"))
    #     test_targets.append(rating)
    #
    # print(
    #     f"--MOVIE--\nMSE train: {cf.mean_squared_error(training_predictions, training_targets)}"
    # )
    # print(f"MSE test: {cf.mean_squared_error(test_predictions, test_targets)}\n--USER--")

    cf.averages = None
    cf.neighbours = None
    cf.deviations = None
    training_predictions = []
    training_targets = []
    for (u, m), rating in usermovie2rating.items():
            training_predictions.append(cf.predict(u, m, "user"))
            training_targets.append(rating)

    for (u, m), rating in usermovie2rating_test.items():
        test_predictions.append(cf.predict(u, m, "user"))
        test_targets.append(rating)

    print(
        f"MSE train: {cf.mean_squared_error(training_predictions, training_targets)}"
    )
    print(f"MSE test: {cf.mean_squared_error(test_predictions, test_targets)}")
