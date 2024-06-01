package github.mmusica.controller;

import github.mmusica.model.Product;
import github.mmusica.rest.RecommenderService;
import github.mmusica.service.ProductService;
import jakarta.enterprise.context.RequestScoped;
import jakarta.inject.Inject;
import jakarta.ws.rs.GET;
import jakarta.ws.rs.POST;
import jakarta.ws.rs.Path;
import org.eclipse.microprofile.rest.client.inject.RestClient;

import java.util.List;

@Path("/product")
@RequestScoped
public class ProductEndpoint {

    @Inject
    ProductService productService;

    @RestClient
    RecommenderService recommenderService;

    @GET
    @Path("")
    public List<Product> getAllProducts() {
        return productService.getAllProducts();
    }

    @POST
    @Path("")
    public void addProduct(Product product) {
        productService.addProduct(product);
    }

    @GET
    @Path("/py_test")
    public String getPyTest() {
        return recommenderService.helloTest();
    }
}
