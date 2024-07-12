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
    @Path("/collaborative_filtering/movie-movie")
    List<MovieRatingDto> getMovieTopN(@QueryParam("userId") Long userId, @QueryParam("count") Integer count);
}
