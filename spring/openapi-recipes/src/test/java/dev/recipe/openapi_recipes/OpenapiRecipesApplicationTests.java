package dev.recipe.openapi_recipes;

import dev.recipe.openapi_recipes.client.ApiClient;
import dev.recipe.openapi_recipes.client.DefaultApi;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;

@SpringBootTest
class OpenapiRecipesApplicationTests {

	@Autowired
	ApiClient apiClient;

	@Test
	void contextLoads() {
		new DefaultApi(apiClient);
	}

}
