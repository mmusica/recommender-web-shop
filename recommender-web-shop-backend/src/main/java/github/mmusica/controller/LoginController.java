package github.mmusica.controller;

import github.mmusica.dto.UserLoginDto;
import github.mmusica.service.UserService;
import jakarta.enterprise.context.RequestScoped;
import jakarta.inject.Inject;
import jakarta.ws.rs.POST;
import jakarta.ws.rs.Path;
import jakarta.ws.rs.QueryParam;

@RequestScoped
@Path("login")
public class LoginController {

    @Inject
    UserService userService;

    @POST
    @Path("")
    public Long login(UserLoginDto loginDto) {
        return userService.findUserByUsername(loginDto.getUsername());
    }
}
