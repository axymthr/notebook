package dev.recipe.openapi_recipes;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

@SpringBootApplication
public class OpenapiRecipesApplication {

	public static void main(String[] args) {
		SpringApplication.run(OpenapiRecipesApplication.class, args);
	}

}

@RestController
@RequestMapping("/manual")
class ManualController {
	@GetMapping(produces = "application/json")
	public Model hello() {
		return new Model("Hello World");
	}
}

class Model {
	private String value;

	public Model(String value) {
		this.value = value;
	}

	public String getValue() {
		return value;
	}

	public void setValue(String value) {
		this.value = value;
	}

	@Override
	public String toString() {
		return "Model{" +
				"value='" + value + '\'' +
				'}';
	}
}