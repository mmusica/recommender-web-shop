package github.mmusica.repository;

import github.mmusica.model.Genre;
import io.quarkus.hibernate.orm.panache.PanacheRepository;
import jakarta.enterprise.context.ApplicationScoped;

import java.util.Optional;

@ApplicationScoped
public class GenreRepository implements PanacheRepository<Genre> {

    public Optional<Genre> findByName(String genreName) {
        return this.find("WHERE name = ?1", genreName).singleResultOptional();
    }
}
