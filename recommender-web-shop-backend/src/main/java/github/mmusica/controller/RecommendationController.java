package github.mmusica.controller;

import github.mmusica.dto.MovieNameRatingDto;
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
    @Path("/collaborative_filtering/movie-movie")
    public List<MovieNameRatingDto> getTopNMoviesForUserMovieCf(@QueryParam("userId") Long userId, @QueryParam("count") Integer count) {
        return recommenderService.getTopNMoviesForUser(userId, count);
    }

    @GET
    @Path("/collaborative_filtering/user-user")
    public List<MovieNameRatingDto> getTopNMoviesForUserUserCf(@QueryParam("userId") Long userId, @QueryParam("count") Integer count) {
        return recommenderService.getTopNMoviesForUserCfUser(userId, count);
    }

    @GET
    @Path("/matrix-factorization/ALS")
    public List<MovieNameRatingDto> getTopNMoviesMfALS(@QueryParam("userId") Long userId, @QueryParam("count") Integer count) {
        return recommenderService.getTopNMoviesMfALS(userId, count);
    }


    @GET
    @Path("/neural-network")
    public List<MovieNameRatingDto> getTopNMoviesDnn(@QueryParam("userId") Long userId, @QueryParam("count") Integer count) {
        return recommenderService.getTopNMoviesDnn(userId, count);
    }

    @GET
    @Path("/neural-network/batch")
    public List<MovieNameRatingDto> getTopNMoviesDnnBatch(@QueryParam("userId") Long userId, @QueryParam("count") Integer count) {
        return recommenderService.getTopNMoviesDnnBatch(userId, count);
    }
}
