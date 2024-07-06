package github.mmusica.repository;

import github.mmusica.model.Movie;
import io.quarkus.hibernate.orm.panache.PanacheRepository;
import jakarta.enterprise.context.ApplicationScoped;

import java.util.Optional;

@ApplicationScoped
public class MovieRepository implements PanacheRepository<Movie> {

    public Optional<Movie> findByName(String name){
        return this.find("WHERE name = ?1", name).singleResultOptional();
    }

    public Optional<Movie> findByIndx(Long movie_indx){
        return this.find("WHERE movieIndx = ?1", movie_indx).singleResultOptional();
    }
}
