package github.mmusica.rest;

import jakarta.ws.rs.GET;
import jakarta.ws.rs.Path;
import org.eclipse.microprofile.rest.client.inject.RegisterRestClient;

@RegisterRestClient(configKey = "recommender-api")
public interface RecommenderService {

    @GET
    @Path("")
    String helloTest();
}
