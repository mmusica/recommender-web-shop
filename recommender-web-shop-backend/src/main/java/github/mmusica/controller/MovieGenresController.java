package github.mmusica.controller;

import github.mmusica.event.LoadEvent;
import jakarta.enterprise.context.RequestScoped;
import jakarta.enterprise.event.Event;
import jakarta.inject.Inject;
import jakarta.ws.rs.GET;
import jakarta.ws.rs.Path;

@RequestScoped
@Path("movieGenres")
public class MovieGenresController {

    @Inject
    Event<LoadEvent> event;

    @GET
    @Path("/loadData")
    public String loadMovieGenresToDatabase(){
        event.fireAsync(new LoadEvent());
        return "Loaded";
    }
}
