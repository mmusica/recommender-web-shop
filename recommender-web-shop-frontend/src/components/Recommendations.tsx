import { useEffect, useState } from "react";
import { useAuth } from "../context/AuthContext"; // Adjust the import path as needed
import {
  fetchMoviePoster,
  fetchRecommendationsMovieCf,
  fetchRecommendationsUserCf,
  fetchRecommendationsMfALS,
  fetchRecommendationsDnnBatch,
  fetchLikedMovies,
} from "../api/api";

interface Movie {
  movieId: number;
  rating: number;
  name: string;
  genres: string[];
  posterPath?: string;
}

interface Recommendations {
  likedMovies: Movie[];
  movieCf: Movie[];
  userCf: Movie[];
  mfAls: Movie[];
  dnnBatch: Movie[];
}

function Recommendations() {
  const { userId } = useAuth();
  const [recommendations, setRecommendations] = useState<Recommendations>({
    likedMovies: [],
    movieCf: [],
    userCf: [],
    mfAls: [],
    dnnBatch: [],
  });
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

  const OMDB_API_KEY = "59ee04ee477ef6a2b5e5bae0263fe2e5";
  const COUNT = 8;

  useEffect(() => {
    if (!userId) {
      setError("User ID is not available.");
      setLoading(false);
      return;
    }

    const fetchAllRecommendations = async () => {
      const recommendationsWithPosters: Recommendations = {
        likedMovies: [],
        movieCf: [],
        userCf: [],
        mfAls: [],
        dnnBatch: [],
      };
      const cleanTitle = (title: string) => {
        return title.replace(/\s*\([^)]*\)/g, "").trim();
      };

      try {
        // Fetch recommendations from all four endpoints
        const [likedMovies, movieCf, userCf, mfAls, dnnBatch] =
          await Promise.all([
            fetchLikedMovies(userId, COUNT).catch(() => []),
            fetchRecommendationsMovieCf(userId, COUNT).catch(() => []),
            fetchRecommendationsUserCf(userId, COUNT).catch(() => []),
            fetchRecommendationsMfALS(userId, COUNT).catch(() => []),
            fetchRecommendationsDnnBatch(userId, COUNT).catch(() => []),
          ]);

        recommendationsWithPosters.likedMovies = likedMovies;
        recommendationsWithPosters.movieCf = movieCf;
        recommendationsWithPosters.userCf = userCf;
        recommendationsWithPosters.mfAls = mfAls;
        recommendationsWithPosters.dnnBatch = dnnBatch;

        const fetchPosters = async (movies: Movie[]) => {
          return Promise.all(
            movies.map(async (movie: Movie) => {
              try {
                const posterData = await fetchMoviePoster(
                  cleanTitle(movie.name),
                  OMDB_API_KEY
                );
                const posterPath = posterData?.results[0]?.poster_path
                  ? "https://image.tmdb.org/t/p/w500" +
                    posterData.results[0].poster_path
                  : "";
                return { ...movie, posterPath };
              } catch (err) {
                console.error(
                  `Error fetching poster for movie: ${movie.name}`,
                  err
                );
                return { ...movie, posterPath: "" };
              }
            })
          );
        };

        recommendationsWithPosters.likedMovies = await fetchPosters(
          recommendationsWithPosters.likedMovies
        );
        recommendationsWithPosters.movieCf = await fetchPosters(
          recommendationsWithPosters.movieCf
        );
        recommendationsWithPosters.userCf = await fetchPosters(
          recommendationsWithPosters.userCf
        );
        recommendationsWithPosters.mfAls = await fetchPosters(
          recommendationsWithPosters.mfAls
        );
        recommendationsWithPosters.dnnBatch = await fetchPosters(
          recommendationsWithPosters.dnnBatch
        );

        setRecommendations(recommendationsWithPosters);
      } catch (error) {
        console.error("Error fetching recommendations or posters:", error);
        setError("Failed to fetch movie recommendations.");
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
        <h3>User Liked Movies</h3>
        <div className="row">
          {recommendations.likedMovies.map((movie) => (
            <div className="col-md-3 mb-3" key={movie.movieId}>
              <div className="card">
                {movie.posterPath ? (
                  <img
                    src={movie.posterPath}
                    className="card-img-top"
                    alt={movie.name}
                    style={{ height: "400px", objectFit: "cover" }}
                  />
                ) : (
                  <div
                    className="card-img-top d-flex align-items-center justify-content-center"
                    style={{ height: "400px", backgroundColor: "#f0f0f0" }}
                  >
                    <span>No Image Available</span>
                  </div>
                )}
                <div className="card-body">
                  <h5 className="card-title">{movie.name}</h5>
                  <p className="card-text">Rating: {movie.rating}</p>
                  {movie.genres && movie.genres.length > 0 && (
                    <p className="card-text">
                      <strong>Genres: </strong>
                      {movie.genres.join(", ")}
                    </p>
                  )}
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>

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
                    style={{ height: "400px", objectFit: "cover" }}
                  />
                ) : (
                  <div
                    className="card-img-top d-flex align-items-center justify-content-center"
                    style={{ height: "400px", backgroundColor: "#f0f0f0" }}
                  >
                    <span>No Image Available</span>
                  </div>
                )}
                <div className="card-body">
                  <h5 className="card-title">{movie.name}</h5>
                  <p className="card-text">Rating: {movie.rating}</p>
                  {movie.genres && movie.genres.length > 0 && (
                    <p className="card-text">
                      <strong>Genres: </strong>
                      {movie.genres.join(", ")}
                    </p>
                  )}
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
                    style={{ height: "400px", objectFit: "cover" }}
                  />
                ) : (
                  <div
                    className="card-img-top d-flex align-items-center justify-content-center"
                    style={{ height: "400px", backgroundColor: "#f0f0f0" }}
                  >
                    <span>No Image Available</span>
                  </div>
                )}
                <div className="card-body">
                  <h5 className="card-title">{movie.name}</h5>
                  <p className="card-text">Rating: {movie.rating}</p>
                  {movie.genres && movie.genres.length > 0 && (
                    <p className="card-text">
                      <strong>Genres: </strong>
                      {movie.genres.join(", ")}
                    </p>
                  )}
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
                    style={{ height: "400px", objectFit: "cover" }}
                  />
                ) : (
                  <div
                    className="card-img-top d-flex align-items-center justify-content-center"
                    style={{ height: "400px", backgroundColor: "#f0f0f0" }}
                  >
                    <span>No Image Available</span>
                  </div>
                )}
                <div className="card-body">
                  <h5 className="card-title">{movie.name}</h5>
                  <p className="card-text">Rating: {movie.rating}</p>
                  {movie.genres && movie.genres.length > 0 && (
                    <p className="card-text">
                      <strong>Genres: </strong>
                      {movie.genres.join(", ")}
                    </p>
                  )}
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
                    style={{ height: "400px", objectFit: "cover" }}
                  />
                ) : (
                  <div
                    className="card-img-top d-flex align-items-center justify-content-center"
                    style={{ height: "400px", backgroundColor: "#f0f0f0" }}
                  >
                    <span>No Image Available</span>
                  </div>
                )}
                <div className="card-body">
                  <h5 className="card-title">{movie.name}</h5>
                  <p className="card-text">Rating: {movie.rating}</p>
                  {movie.genres && movie.genres.length > 0 && (
                    <p className="card-text">
                      <strong>Genres: </strong>
                      {movie.genres.join(", ")}
                    </p>
                  )}
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
