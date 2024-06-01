package github.mmusica.controller;

import github.mmusica.model.Product;
import github.mmusica.service.ProductService;
import jakarta.enterprise.context.RequestScoped;
import jakarta.ws.rs.GET;
import jakarta.ws.rs.POST;
import jakarta.ws.rs.Path;
import lombok.AllArgsConstructor;

import java.util.List;

@Path("/product")
@RequestScoped
@AllArgsConstructor
public class ProductEndpoint {

    ProductService productService;

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
}
