package github.mmusica.service;

import github.mmusica.dto.MovieNameRatingDto;
import github.mmusica.model.Movie;
import github.mmusica.model.UserMovieRating;
import github.mmusica.repository.UserMovieRatingRepository;
import jakarta.enterprise.context.ApplicationScoped;
import jakarta.inject.Inject;

import java.util.List;

@ApplicationScoped
public class MovieService {

    @Inject
    UserMovieRatingRepository userMovieRatingRepository;

    public List<MovieNameRatingDto> getTopNMoviesForUser(Long userId, Integer count) {
        List<UserMovieRating> byUserIdCount = userMovieRatingRepository.findByUserIdCount(userId, count);
        return byUserIdCount.stream().map(userMovieRating ->
                MovieNameRatingDto.builder()
                        .movieId(userMovieRating.getMovie().getId())
                        .genres(getGenreStrings(userMovieRating.getMovie()))
                        .name(userMovieRating.getMovie().getName())
                        .rating(userMovieRating.getRating())
                        .build()
        ).toList();
    }

    private List<String> getGenreStrings(Movie movie) {
        return movie.getMovieGenres().stream().map(it -> it.getGenre().getName()).toList();
    }
}
