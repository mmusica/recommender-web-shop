package github.mmusica.rest;

import github.mmusica.dto.MovieRatingDto;
import jakarta.ws.rs.GET;
import jakarta.ws.rs.Path;
import jakarta.ws.rs.QueryParam;
import org.eclipse.microprofile.rest.client.inject.RegisterRestClient;

import java.util.List;

@RegisterRestClient(configKey = "recommender-api")
public interface RecommenderClient {

    @GET
    @Path("/collaborative-filtering/movie-movie")
    List<MovieRatingDto> getMovieTopN(@QueryParam("userId") Long userId, @QueryParam("count") Integer count);

    @GET
    @Path("/collaborative-filtering/user-user")
    List<MovieRatingDto> getUserTopN(@QueryParam("userId") Long userId, @QueryParam("count") Integer count);


    @GET
    @Path("/matrix-factorization/ALS")
    List<MovieRatingDto> getMovieTopNMatrixFactorization(@QueryParam("userId") Long userId, @QueryParam("count") Integer count);

    @GET
    @Path("/deep-neural-network")
    List<MovieRatingDto> getMovieTopNDeepNeuralNetwork(@QueryParam("userId") Long userId, @QueryParam("count") Integer count);

    @GET
    @Path("/deep-neural-network/batch")
    List<MovieRatingDto> getMovieTopNDeepNeuralNetworkBatch(@QueryParam("userId") Long userId, @QueryParam("count") Integer count);
}
