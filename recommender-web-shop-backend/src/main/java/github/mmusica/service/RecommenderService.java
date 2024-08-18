package github.mmusica.service;

import github.mmusica.dto.MovieNameRatingDto;
import github.mmusica.dto.MovieRatingDto;
import github.mmusica.model.Movie;
import github.mmusica.repository.MovieRepository;
import github.mmusica.rest.RecommenderClient;
import jakarta.enterprise.context.ApplicationScoped;
import jakarta.inject.Inject;
import org.eclipse.microprofile.rest.client.inject.RestClient;

import java.util.List;

@ApplicationScoped
public class RecommenderService {

    @RestClient
    RecommenderClient recommenderClient;

    @Inject
    MovieRepository movieRepository;

    public List<MovieNameRatingDto> getTopNMoviesForUser(Long userId, Integer count) {
        List<MovieRatingDto> movieTopN = recommenderClient.getMovieTopN(userId, count);
        return getMovieNameRatingDtos(movieTopN);
    }

    public List<MovieNameRatingDto> getTopNMoviesForUserCfUser(Long userId, Integer count) {
        List<MovieRatingDto> movieTopN = recommenderClient.getUserTopN(userId, count);
        return getMovieNameRatingDtos(movieTopN);
    }

    public List<MovieNameRatingDto> getTopNMoviesMfALS(Long userId, Integer count) {
        List<MovieRatingDto> movieTopN = recommenderClient.getMovieTopNMatrixFactorization(userId, count);
        return getMovieNameRatingDtos(movieTopN);
    }

    public List<MovieNameRatingDto> getTopNMoviesDnn(Long userId, Integer count) {
        List<MovieRatingDto> movieTopN = recommenderClient.getMovieTopNNeuralNetwork(userId, count);
        return getMovieNameRatingDtos(movieTopN);
    }

    public List<MovieNameRatingDto> getTopNMoviesDnnBatch(Long userId, Integer count) {
        List<MovieRatingDto> movieTopN = recommenderClient.getMovieTopNNeuralNetworkBatch(userId, count);
        return getMovieNameRatingDtos(movieTopN);
    }

    private List<MovieNameRatingDto> getMovieNameRatingDtos(List<MovieRatingDto> movieTopN) {
        return movieTopN.stream().map(movieRatingDto ->
                {
                    Movie byId = movieRepository.findById(movieRatingDto.getMovieId());
                    return MovieNameRatingDto.builder()
                            .movieId(movieRatingDto.getMovieId())
                            .rating(movieRatingDto.getRating())
                            .name(byId.getName())
                            .genres(getGenreStrings(byId))
                            .build();
                }
        ).toList();
    }

    private List<String> getGenreStrings(Movie byId) {
        return byId.getMovieGenres().stream().map(it -> it.getGenre().getName()).toList();
    }
}
