package github.mmusica.controller;

import github.mmusica.dto.MovieNameRatingDao;
import github.mmusica.dto.MovieRatingDto;
import github.mmusica.service.RecommenderService;
import jakarta.enterprise.context.RequestScoped;
import jakarta.inject.Inject;
import jakarta.ws.rs.GET;
import jakarta.ws.rs.Path;
import jakarta.ws.rs.QueryParam;

import java.util.List;

@RequestScoped
@Path("recommender")
public class RecommendationController {

    @Inject
    RecommenderService recommenderService;

    @GET
    @Path("/collaborative_filtering")
    public List<MovieNameRatingDao> getTopNMoviesForUser(@QueryParam("userId") Long userId, @QueryParam("count") Integer count) {
        return recommenderService.getTopNMoviesForUser(userId, count);
    }
}
