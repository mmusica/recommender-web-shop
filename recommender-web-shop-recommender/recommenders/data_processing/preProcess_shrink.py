from typing import Counter

import pandas as pd


def get_new_ids(old_ids):
    i = 0
    new_ids = {}
    for id in old_ids:
        new_ids[id] = i
        i += 1
    return new_ids


if __name__ == "__main__":
    processed_ratings = pd.read_csv('../large_files/movielens-20m-dataset/edited_ratings.csv')

    num_of_users = processed_ratings.userId.max() + 1
    num_of_movies = processed_ratings.movie_indx.max() + 1

    user_ids_count = Counter(processed_ratings.userId)
    movie_idx_count = Counter(processed_ratings.movie_indx)

    num_of_keep_users = 1000
    num_of_keep_movies = 2000

    user_ids = [u for u, c in user_ids_count.most_common(num_of_keep_users)]
    movie_idxs = [m for m, c in movie_idx_count.most_common(num_of_keep_movies)]

    processed_ratings_small = processed_ratings[processed_ratings.userId.isin(user_ids) &
                                                processed_ratings.movie_indx.isin(movie_idxs)].copy()

    new_movie_ids = get_new_ids(movie_idxs)
    new_user_ids = get_new_ids(user_ids)

    processed_ratings_small.loc[:, 'userId'] = processed_ratings_small.apply(lambda row: new_user_ids[row.userId],
                                                                             axis='columns')
    processed_ratings_small.loc[:, 'movie_indx'] = processed_ratings_small.apply(
        lambda row: new_movie_ids[row.movie_indx], axis='columns')

    print(f"Max user id: {processed_ratings_small.userId.max()}")
    print(f"Max movie id: {processed_ratings_small.movie_indx.max()}")

    print(f"Small dataset size:", len(processed_ratings_small))

    processed_ratings_small.to_csv('../large_files/movielens-20m-dataset/small_rating.csv', index=False)

    movie_df = pd.read_csv('../large_files/movielens-20m-dataset/movie.csv')
    merged_df = movie_df.merge(processed_ratings_small, on='movieId', how='right')
    merged_df = merged_df.drop_duplicates(subset=['title'])
    merged_df.to_csv('../large_files/movielens-20m-dataset/merged.csv', index=False, sep=';')
