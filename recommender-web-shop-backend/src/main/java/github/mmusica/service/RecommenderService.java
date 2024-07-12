package github.mmusica.service;

import github.mmusica.dto.MovieNameRatingDao;
import github.mmusica.dto.MovieRatingDto;
import github.mmusica.repository.MovieRepository;
import github.mmusica.rest.RecommenderClient;
import jakarta.enterprise.context.ApplicationScoped;
import jakarta.inject.Inject;
import org.eclipse.microprofile.rest.client.inject.RestClient;

import java.util.ArrayList;
import java.util.List;

import static java.util.stream.Collectors.toList;

@ApplicationScoped
public class RecommenderService {

    @RestClient
    RecommenderClient recommenderClient;

    @Inject
    MovieRepository movieRepository;

    public List<MovieNameRatingDao> getTopNMoviesForUser(Long userId, Integer count) {
        List<MovieRatingDto> movieTopN = recommenderClient.getMovieTopN(userId, count);
        return movieTopN.stream().map(movieRatingDto ->
                MovieNameRatingDao.builder()
                        .movieId(movieRatingDto.getMovieId())
                        .rating(movieRatingDto.getRating())
                        .name(movieRepository.findById(movieRatingDto.getMovieId()).getName())
                        .build()
        ).toList();
    }
}
