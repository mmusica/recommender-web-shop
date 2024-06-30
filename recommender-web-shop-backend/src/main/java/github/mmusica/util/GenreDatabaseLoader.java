package github.mmusica.util;

import github.mmusica.model.Genre;
import github.mmusica.repository.GenreRepository;
import jakarta.enterprise.context.ApplicationScoped;
import jakarta.inject.Inject;
import jakarta.transaction.Transactional;

import java.util.Optional;

@ApplicationScoped
public class GenreDatabaseLoader {

    @Inject
    GenreRepository genreRepository;

    @Transactional
    public Genre createIfNotExists(String genreName) {
        Optional<Genre> genre = genreRepository.findByName(genreName);
        if (genre.isPresent()) {
            return genre.get();
        } else {
            Genre genreToSave = Genre.builder()
                    .name(genreName)
                    .build();
            genreRepository.persist(genreToSave);
            return genreToSave;
        }
    }
}
