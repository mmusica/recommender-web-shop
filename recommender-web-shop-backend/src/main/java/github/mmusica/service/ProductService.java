package github.mmusica.service;

import github.mmusica.model.Product;
import github.mmusica.repository.ProductRepository;
import jakarta.enterprise.context.ApplicationScoped;
import jakarta.transaction.Transactional;
import lombok.AllArgsConstructor;

import java.util.List;

@ApplicationScoped
@AllArgsConstructor
public class ProductService {

    ProductRepository productRepository;

    @Transactional
    public void addProduct(Product product) {
        productRepository.persist(product);
    }

    public List<Product> getAllProducts() {
        return productRepository.listAll();
    }
}
