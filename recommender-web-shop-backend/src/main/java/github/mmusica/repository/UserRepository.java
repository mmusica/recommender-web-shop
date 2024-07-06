package github.mmusica.repository;

import github.mmusica.model.User;
import io.quarkus.hibernate.orm.panache.PanacheRepository;
import jakarta.enterprise.context.ApplicationScoped;

import java.util.Optional;

@ApplicationScoped
public class UserRepository implements PanacheRepository<User> {

    public Optional<User> findByUsername(String username){
        return this.find("WHERE username = ?1", username).singleResultOptional();
    }
}
