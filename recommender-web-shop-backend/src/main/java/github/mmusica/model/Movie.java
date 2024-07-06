package github.mmusica.model;

import jakarta.persistence.*;
import lombok.*;

import java.util.List;
import java.util.Set;

@Entity
@AllArgsConstructor
@NoArgsConstructor
@Builder
@Getter
@Setter
@Table(name = "movie")
public class Movie {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(name = "movie_indx")
    private Long movieIndx;

    @Column(name = "name")
    private String name;

    @OneToMany(mappedBy = "movie")
    private Set<MovieGenre> movieGenres;

    @OneToMany(mappedBy = "movie")
    private List<UserMovieRating> userMovieRatings;
}
