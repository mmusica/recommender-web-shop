import axiosInstance from './axiosInstance';

export const loginUser = async (username: string) => {
  const response = await axiosInstance.post('/login', { username });
  return response.data;
};


export const fetchLikedMovies = async (userId: number, count: number) => {
  const response = await axiosInstance.get('movies', {
    params: { userId, count },
  });
  return response.data;
};

export const fetchRecommendationsMovieCf = async (userId: number, count: number) => {
  const response = await axiosInstance.get('recommender/collaborative_filtering/movie-movie', {
    params: { userId, count },
  });
  return response.data;
};

export const fetchRecommendationsUserCf = async (userId: number, count: number) => {
  const response = await axiosInstance.get('recommender/collaborative_filtering/user-user', {
    params: { userId, count },
  });
  return response.data;
};

export const fetchRecommendationsMfALS = async (userId: number, count: number) => {
  const response = await axiosInstance.get('recommender/matrix-factorization/ALS', {
    params: { userId, count },
  });
  return response.data;
};

export const fetchRecommendationsDnnBatch = async (userId: number, count: number) => {
  const response = await axiosInstance.get('recommender/neural-network/batch', {
    params: { userId, count },
  });
  return response.data;
};


// Function to fetch movie details including poster from TMDB API
export const fetchMoviePoster = async (title: string, apiKey: string) => {
  const response = await axiosInstance.get(
    `https://api.themoviedb.org/3/search/movie?api_key=${apiKey}&query=${encodeURIComponent(title)}&page=1&include_adult=false`
  );
  return response.data;
};
