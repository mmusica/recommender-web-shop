package github.mmusica.repository;

import github.mmusica.model.UserMovieRating;
import io.quarkus.hibernate.orm.panache.PanacheRepository;
import jakarta.enterprise.context.ApplicationScoped;

import java.util.List;

@ApplicationScoped
public class UserMovieRatingRepository implements PanacheRepository<UserMovieRating> {

    public List<UserMovieRating> findByUserIdCount(Long userId, Integer count) {
        if (count == null) {
            count = 8;
        }
        return find("WHERE user.id = ?1 order by rating DESC", userId).page(0, count).stream().toList();
    }
}
