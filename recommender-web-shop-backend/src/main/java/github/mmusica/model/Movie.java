package github.mmusica.model;

import jakarta.persistence.*;
import lombok.*;

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

    @Column(name = "movie_id")
    private Long movie_id;

    @Column(name = "name")
    private String name;

    @OneToMany(mappedBy = "movie")
    private Set<MovieGenre> movieGenres;
}
