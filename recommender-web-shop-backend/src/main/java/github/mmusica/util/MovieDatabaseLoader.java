package github.mmusica.util;

import github.mmusica.event.LoadMovieGeneresEvent;
import github.mmusica.model.Genre;
import github.mmusica.model.Movie;
import github.mmusica.model.MovieGenre;
import github.mmusica.repository.MovieGenreRepository;
import github.mmusica.repository.MovieRepository;
import jakarta.enterprise.context.ApplicationScoped;
import jakarta.enterprise.event.ObservesAsync;
import jakarta.inject.Inject;
import jakarta.transaction.Transactional;
import lombok.extern.slf4j.Slf4j;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.util.*;
import java.util.stream.Collectors;

@ApplicationScoped
@Slf4j
public class MovieDatabaseLoader {

    private static int ID = 0;
    private static int TITLE = 1;
    private static int GENRES = 2;
    private static int INDX = 5;

    @Inject
    GenreDatabaseLoader genreDatabaseLoader;

    @Inject
    MovieGenreRepository movieGenreRepository;

    @Inject
    MovieRepository movieRepository;

    @Transactional
    public void loadMoviesIntoDatabase(@ObservesAsync LoadMovieGeneresEvent loadMovieGeneresEvent) {
        int i = 0;
        try (BufferedReader br = new BufferedReader(getInputStreamReader())) {
            String line;
            while ((line = br.readLine()) != null) {

                if (i == 0) {
                    i++;
                    continue;
                }
                String[] values = line.split(";");
                Movie movie = convertToMovie(values);
                Set<Genre> genres = convertToGenres(values[GENRES]);
                Set<MovieGenre> movieGenres = convertToMovieGenres(movie, genres);
                movieRepository.persist(movie);
                movieGenreRepository.persist(movieGenres);
                log.info("Done: {}", i);
                i++;
            }
        } catch (IOException e) {
            throw new RuntimeException(e);
        }
        log.info("All movies inserted");
    }

    private InputStreamReader getInputStreamReader() {
        return new InputStreamReader(getClass().getClassLoader().getResourceAsStream("merged.csv"));
    }

    private Movie convertToMovie(String[] values) {
        return Movie.builder()
                .movie_id(Long.parseLong(values[INDX]))
                .name(values[TITLE])
                .build();
    }

    private Set<Genre> convertToGenres(String value) {
        Set<Genre> genres = new HashSet<>();
        String[] genresStrings = value.split("\\|");
        Arrays.stream(genresStrings).forEach(s -> genres.add(genreDatabaseLoader.createIfNotExists(s)));
        return genres;
    }

    private static Set<MovieGenre> convertToMovieGenres(Movie movie, Set<Genre> genres) {
        return genres.stream().map(genre ->
                MovieGenre.builder()
                        .genre(genre)
                        .movie(movie)
                        .build()
        ).collect(Collectors.toSet());
    }
}
