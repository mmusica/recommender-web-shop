import pandas as pd

if __name__ == "__main__":
    ratings = pd.read_csv("../large_files/movielens-20m-dataset/rating.csv")

    ratings.userId = ratings.userId - 1
    unique_movies_id = set(ratings.movieId)

    new_movie_ids = {}

    count = 0
    for movie_id in unique_movies_id:
        new_movie_ids[movie_id] = count
        count += 1

    ratings['movie_indx'] = ratings.apply(lambda row: new_movie_ids[row.movieId], axis='columns')
    ratings = ratings.drop(columns=['timestamp'])

    ratings.to_csv("../large_files/movielens-20m-dataset/edited_ratings.csv", sep=',', index=False)
