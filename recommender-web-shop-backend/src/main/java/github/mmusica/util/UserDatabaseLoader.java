package github.mmusica.util;

import github.mmusica.event.LoadUserRatingsEvent;
import jakarta.enterprise.context.ApplicationScoped;
import jakarta.enterprise.event.ObservesAsync;

@ApplicationScoped
public class UserDatabaseLoader {

    public void loadUsersToDatabase(@ObservesAsync LoadUserRatingsEvent loadUserRatingsEvent){

    }
}
