package github.mmusica.controller;

import github.mmusica.event.LoadUserRatingsEvent;
import jakarta.enterprise.context.RequestScoped;
import jakarta.enterprise.event.Event;
import jakarta.inject.Inject;
import jakarta.ws.rs.GET;
import jakarta.ws.rs.Path;

@RequestScoped
@Path("userMovieRatings")
public class UserMovieRatingsController {

    @Inject
    Event<LoadUserRatingsEvent> usersEvent;

    @GET
    @Path("loadData")
    public String loadUserRatingsToDatabase() {
        usersEvent.fireAsync(new LoadUserRatingsEvent());
        return "Loading users, be patient....";
    }
}
