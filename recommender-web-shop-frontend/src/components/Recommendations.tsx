import { useEffect, useState } from 'react';
import { useAuth } from '../context/AuthContext'; // Adjust the import path as needed
import { fetchMoviePoster, fetchRecommendationsMovieCf, fetchRecommendationsUserCf, fetchRecommendationsMfALS, fetchRecommendationsDnnBatch } from '../api/api';

interface Movie {
  movieId: number;
  rating: number;
  name: string;
  posterPath?: string;
}

interface Recommendations {
  movieCf: Movie[];
  userCf: Movie[];
  mfAls: Movie[];
  dnnBatch: Movie[];
}

function Recommendations() {
  const { userId } = useAuth();
  const [recommendations, setRecommendations] = useState<Recommendations>({
    movieCf: [],
    userCf: [],
    mfAls: [],
    dnnBatch: []
  });
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

  const OMDB_API_KEY = 'ead0edad';
  const COUNT = 5;

  useEffect(() => {
    if (!userId) {
      setError('User ID is not available.');
      setLoading(false);
      return;
    }

    const fetchAllRecommendations = async () => {
      const recommendationsWithPosters: Recommendations = {
        movieCf: [],
        userCf: [],
        mfAls: [],
        dnnBatch: []
      };

      try {
        // Fetch recommendations from all four endpoints
        const [movieCf, userCf, mfAls, dnnBatch] = await Promise.all([
          fetchRecommendationsMovieCf(userId, COUNT).catch(() => []),
          fetchRecommendationsUserCf(userId, COUNT).catch(() => []),
          fetchRecommendationsMfALS(userId, COUNT).catch(() => []),
          fetchRecommendationsDnnBatch(userId, COUNT).catch(() => [])
        ]);

        recommendationsWithPosters.movieCf = movieCf;
        recommendationsWithPosters.userCf = userCf;
        recommendationsWithPosters.mfAls = mfAls;
        recommendationsWithPosters.dnnBatch = dnnBatch;

        const fetchPosters = async (movies: Movie[]) => {
          return Promise.all(
            movies.map(async (movie: Movie) => {
              try {
                const posterData = await fetchMoviePoster(movie.name, OMDB_API_KEY);
                const posterPath = posterData.Poster !== 'N/A' ? posterData.Poster : '';
                return { ...movie, posterPath };
              } catch (err) {
                console.error(`Error fetching poster for movie: ${movie.name}`, err);
                return { ...movie, posterPath: '' };
              }
            })
          );
        };

        recommendationsWithPosters.movieCf = await fetchPosters(recommendationsWithPosters.movieCf);
        recommendationsWithPosters.userCf = await fetchPosters(recommendationsWithPosters.userCf);
        recommendationsWithPosters.mfAls = await fetchPosters(recommendationsWithPosters.mfAls);
        recommendationsWithPosters.dnnBatch = await fetchPosters(recommendationsWithPosters.dnnBatch);

        setRecommendations(recommendationsWithPosters);
      } catch (error) {
        console.error('Error fetching recommendations or posters:', error);
        setError('Failed to fetch movie recommendations.');
      } finally {
        setLoading(false);
      }
    };

    fetchAllRecommendations();
  }, [userId, OMDB_API_KEY]);

  if (loading) {
    return <div className="container mt-5">Loading...</div>;
  }

  if (error) {
    return <div className="container mt-5 text-danger">{error}</div>;
  }

  return (
    <div className="container mt-5">
      <h2>Movie Recommendations</h2>

      <div className="section">
        <h3>Movie-Movie Collaborative Filtering</h3>
        <div className="row">
          {recommendations.movieCf.map((movie) => (
            <div className="col-md-3 mb-3" key={movie.movieId}>
              <div className="card">
                {movie.posterPath ? (
                  <img
                    src={movie.posterPath}
                    className="card-img-top"
                    alt={movie.name}
                    style={{ height: '200px', objectFit: 'cover' }}
                  />
                ) : (
                  <div className="card-img-top d-flex align-items-center justify-content-center" style={{ height: '200px', backgroundColor: '#f0f0f0' }}>
                    <span>No Image Available</span>
                  </div>
                )}
                <div className="card-body">
                  <h5 className="card-title">{movie.name}</h5>
                  <p className="card-text">Rating: {movie.rating}</p>
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>

      <div className="section">
        <h3>User-User Collaborative Filtering</h3>
        <div className="row">
          {recommendations.userCf.map((movie) => (
            <div className="col-md-3 mb-3" key={movie.movieId}>
              <div className="card">
                {movie.posterPath ? (
                  <img
                    src={movie.posterPath}
                    className="card-img-top"
                    alt={movie.name}
                    style={{ height: '200px', objectFit: 'cover' }}
                  />
                ) : (
                  <div className="card-img-top d-flex align-items-center justify-content-center" style={{ height: '200px', backgroundColor: '#f0f0f0' }}>
                    <span>No Image Available</span>
                  </div>
                )}
                <div className="card-body">
                  <h5 className="card-title">{movie.name}</h5>
                  <p className="card-text">Rating: {movie.rating}</p>
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>

      <div className="section">
        <h3>Matrix Factorization ALS</h3>
        <div className="row">
          {recommendations.mfAls.map((movie) => (
            <div className="col-md-3 mb-3" key={movie.movieId}>
              <div className="card">
                {movie.posterPath ? (
                  <img
                    src={movie.posterPath}
                    className="card-img-top"
                    alt={movie.name}
                    style={{ height: '200px', objectFit: 'cover' }}
                  />
                ) : (
                  <div className="card-img-top d-flex align-items-center justify-content-center" style={{ height: '200px', backgroundColor: '#f0f0f0' }}>
                    <span>No Image Available</span>
                  </div>
                )}
                <div className="card-body">
                  <h5 className="card-title">{movie.name}</h5>
                  <p className="card-text">Rating: {movie.rating}</p>
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>

      <div className="section">
        <h3>Neural Network Batch</h3>
        <div className="row">
          {recommendations.dnnBatch.map((movie) => (
            <div className="col-md-3 mb-3" key={movie.movieId}>
              <div className="card">
                {movie.posterPath ? (
                  <img
                    src={movie.posterPath}
                    className="card-img-top"
                    alt={movie.name}
                    style={{ height: '200px', objectFit: 'cover' }}
                  />
                ) : (
                  <div className="card-img-top d-flex align-items-center justify-content-center" style={{ height: '200px', backgroundColor: '#f0f0f0' }}>
                    <span>No Image Available</span>
                  </div>
                )}
                <div className="card-body">
                  <h5 className="card-title">{movie.name}</h5>
                  <p className="card-text">Rating: {movie.rating}</p>
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}

export default Recommendations;
