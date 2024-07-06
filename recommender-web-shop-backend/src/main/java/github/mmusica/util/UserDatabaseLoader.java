package github.mmusica.util;

import github.mmusica.event.LoadUserRatingsEvent;
import github.mmusica.model.Movie;
import github.mmusica.model.User;
import github.mmusica.model.UserMovieRating;
import github.mmusica.repository.MovieRepository;
import github.mmusica.repository.UserMovieRatingRepository;
import github.mmusica.repository.UserRepository;
import jakarta.enterprise.context.ApplicationScoped;
import jakarta.enterprise.event.ObservesAsync;
import jakarta.inject.Inject;
import jakarta.transaction.Transactional;
import jakarta.ws.rs.NotFoundException;
import lombok.extern.slf4j.Slf4j;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.util.*;

@ApplicationScoped
@Slf4j
public class UserDatabaseLoader {

    private static int USER_ID = 0;
    private static int MOVIE_ID = 1;
    private static int RATING = 2;
    private static int INDX = 3;

    @Inject
    MovieRepository movieRepository;

    @Inject
    UserMovieRatingRepository userMovieRatingRepository;

    @Inject
    UserRepository userRepository;

    public void loadUsersToDatabase(@ObservesAsync LoadUserRatingsEvent loadUserRatingsEvent) {
        int i = 0;
        List<UserMovieRating> userMovieRatings = new ArrayList<>();
        HashMap<String, User> users = new HashMap<>();
        try (BufferedReader br = new BufferedReader(getInputStreamReader())) {
            String line;
            while ((line = br.readLine()) != null) {

                if (i == 0) {
                    i++;
                    continue;
                }
                String[] values = line.split(",");
                User user = convertToUser(values);
                users.put(user.getUsername(), user);
                Movie movie = movieRepository.findByIndx(Long.parseLong(values[INDX])).orElse(null);
                if (movie == null) {
                    throw new NotFoundException("Movie like this doesnt exist");
                }
                UserMovieRating entity = convertToUserMovieRating(values, user, movie);
                userMovieRatings.add(entity);

                log.info("Done: {}", i);
                i++;
            }
        } catch (IOException e) {
            throw new RuntimeException(e);
        }

        persistUsers(users);
        persistUserMovieRatings(userMovieRatings);
        log.info("All userMovieRatings loaded");
    }

    void persistUserMovieRatings(List<UserMovieRating> userMovieRatings) {
        userMovieRatings.forEach(userMovieRating -> {
            Optional<User> byUsername = userRepository.findByUsername(userMovieRating.getUser().getUsername());
            userMovieRating.setUser(byUsername.orElse(null));
            Optional<Movie> byIndx = movieRepository.findByIndx(userMovieRating.getMovie().getMovieIndx());
            userMovieRating.setMovie(byIndx.orElse(null));
            persistUserMovieRating(userMovieRating);
        });
    }

    @Transactional
    void persistUserMovieRating(UserMovieRating userMovieRating) {
        userMovieRatingRepository.persist(userMovieRating);
    }

    void persistUsers(HashMap<String, User> users) {
        users.forEach((s, user) -> persistUser(user));
    }

    @Transactional
    void persistUser(User user) {
        userRepository.persist(user);
    }

    private UserMovieRating convertToUserMovieRating(String[] values, User user, Movie movie) {
        return UserMovieRating.builder()
                .rating(Float.parseFloat(values[RATING]))
                .user(user)
                .movie(movie)
                .build();
    }

    private User convertToUser(String[] values) {
        return User.builder()
                .username("user_" + values[USER_ID])
                .build();
    }

    private InputStreamReader getInputStreamReader() {
        return new InputStreamReader(getClass().getClassLoader().getResourceAsStream("small_rating.csv"));
    }
}
