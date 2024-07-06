package github.mmusica.controller;

import github.mmusica.event.LoadMovieGeneresEvent;
import github.mmusica.event.LoadUserRatingsEvent;
import jakarta.enterprise.context.RequestScoped;
import jakarta.enterprise.event.Event;
import jakarta.inject.Inject;
import jakarta.ws.rs.GET;
import jakarta.ws.rs.Path;

@RequestScoped
@Path("movieGenres")
public class MovieGenresController {

    @Inject
    Event<LoadMovieGeneresEvent> moviesEvent;

    @Inject
    Event<LoadUserRatingsEvent> usersEvent;

    @GET
    @Path("/loadData/movies")
    public String loadMovieGenresToDatabase(){
        moviesEvent.fireAsync(new LoadMovieGeneresEvent());
        return "Loading movies, be patient...";
    }

    @GET
    @Path("loadData/userRatings")
    public String loadUserRatingsToDatabase(){
        usersEvent.fireAsync(new LoadUserRatingsEvent());
        return "Loading users, be patient....";
    }
}
