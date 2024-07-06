package github.mmusica.repository;

import github.mmusica.model.UserMovieRating;
import io.quarkus.hibernate.orm.panache.PanacheRepository;
import jakarta.enterprise.context.ApplicationScoped;

@ApplicationScoped
public class UserMovieRatingRepository implements PanacheRepository<UserMovieRating> {
}
