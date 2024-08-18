package github.mmusica.dto;

import github.mmusica.model.Genre;
import lombok.*;

import java.util.List;

@Data
@AllArgsConstructor
@NoArgsConstructor
@Builder
public class MovieNameRatingDto {
    Long movieId;
    Float rating;
    String name;
    List<String> genres;
}
