package github.mmusica.repository;

import github.mmusica.model.MovieGenre;
import io.quarkus.hibernate.orm.panache.PanacheRepository;
import jakarta.enterprise.context.ApplicationScoped;

@ApplicationScoped
public class MovieGenreRepository implements PanacheRepository<MovieGenre> {

}
