package com.example.vaadin;

import com.vaadin.flow.component.grid.Grid;
import com.vaadin.flow.component.html.H1;
import com.vaadin.flow.component.orderedlayout.VerticalLayout;
import com.vaadin.flow.router.Route;
import org.springframework.boot.ApplicationRunner;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.context.annotation.Bean;
import org.springframework.data.repository.ListCrudRepository;
import org.springframework.web.reactive.function.client.WebClient;
import org.springframework.web.reactive.function.client.support.WebClientAdapter;
import org.springframework.web.service.annotation.GetExchange;
import org.springframework.web.service.invoker.HttpServiceProxyFactory;

import java.util.Collection;

interface PostRepository extends ListCrudRepository<Post, Integer> {
}

interface PostApiClient {
    @GetExchange("/posts")
    Collection<Post> getPosts();
}

@SpringBootApplication
public class VaadinApplication {

    public static void main(String[] args) {
        SpringApplication.run(VaadinApplication.class, args);
    }

    @Bean
    PostApiClient client(WebClient.Builder builder) {
        var wca = WebClientAdapter.create(builder.baseUrl("https://jsonplaceholder.typicode.com").build());
        return HttpServiceProxyFactory.builderFor(wca).build().createClient(PostApiClient.class);
    }

    @Bean
    ApplicationRunner postsInitializer(PostApiClient c, PostRepository r) {
        return args -> {
            r.deleteAll();
            r.saveAll(c.getPosts());
            r.findAll().forEach(p -> System.out.println(p.title()));
        };
    }
}

@Route("")
class PostView extends VerticalLayout {
    public PostView(PostRepository repository) {
        var grid = new Grid<>(Post.class);
        grid.addColumn(Post::postId).setHeader("ID");
        grid.addColumn(Post::title).setHeader("Title");
        grid.addColumn(Post::body).setHeader("Text");
        grid.setItems(repository.findAll());

        var h1 = new H1("Data");
        add(h1, grid);
    }
}

