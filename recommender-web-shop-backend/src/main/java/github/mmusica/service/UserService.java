package github.mmusica.service;

import github.mmusica.model.User;
import github.mmusica.repository.UserRepository;
import jakarta.enterprise.context.ApplicationScoped;
import jakarta.inject.Inject;

import java.util.Optional;

@ApplicationScoped
public class UserService {

    @Inject
    UserRepository userRepository;

    public Long findUserByUsername(String username){
        Optional<User> byUsername = userRepository.findByUsername(username);
        if(byUsername.isPresent()){
            return byUsername.get().getId();
        }else {
            return null;
        }
    }
}
