package dev.recipe.openapi_recipes;

import dev.recipe.openapi_recipes.api.GeneratedApi;
import dev.recipe.openapi_recipes.api.Model;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class StandardGeneratedApi implements GeneratedApi {
    @Override
    public ResponseEntity<Model> generatedGet() {
        Model model = new Model();
        model.setValue("Hello Generated World");
        return ResponseEntity.ok(model);
    }
}
