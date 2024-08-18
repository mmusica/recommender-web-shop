package github.mmusica.controller;

import github.mmusica.dto.MovieNameRatingDto;
import github.mmusica.service.MovieService;
import jakarta.enterprise.context.RequestScoped;
import jakarta.inject.Inject;
import jakarta.ws.rs.GET;
import jakarta.ws.rs.Path;
import jakarta.ws.rs.QueryParam;

import java.util.List;

@RequestScoped
@Path("movies")
public class MovieController {

    @Inject
    MovieService movieService;

    @GET
    @Path("")
    public List<MovieNameRatingDto> getTopNMoviesForUser(@QueryParam("userId") Long userId,
                                                         @QueryParam("count") Integer count) {
        return movieService.getTopNMoviesForUser(userId, count);
    }
}
