package github.mmusica.controller;

import github.mmusica.event.LoadMovieGeneresEvent;
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

    @GET
    @Path("/loadData")
    public String loadMovieGenresToDatabase() {
        moviesEvent.fireAsync(new LoadMovieGeneresEvent());
        return "Loading movies, be patient...";
    }
}
