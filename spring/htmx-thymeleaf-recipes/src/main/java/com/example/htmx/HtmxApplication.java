package com.example.htmx;

import io.github.wimdeblauwe.htmx.spring.boot.mvc.HtmxResponse;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.boot.context.event.ApplicationReadyEvent;
import org.springframework.context.ApplicationEvent;
import org.springframework.context.ApplicationEventPublisher;
import org.springframework.context.event.EventListener;
import org.springframework.http.MediaType;
import org.springframework.stereotype.Component;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.servlet.View;
import org.springframework.web.servlet.view.FragmentsRendering;
import org.springframework.data.repository.CrudRepository;

import java.time.Instant;
import java.util.Comparator;
import java.util.Set;
import java.util.concurrent.ConcurrentSkipListSet;
import java.util.concurrent.atomic.AtomicInteger;
import java.util.stream.Stream;

@SpringBootApplication
public class HtmxApplication {

	public static void main(String[] args) {
		SpringApplication.run(HtmxApplication.class, args);
	}

}

@Controller
@RequestMapping("/todos")
class ToDoController{
	private final Set<ToDo> toDos = new ConcurrentSkipListSet<>(Comparator.comparingInt(ToDo::id));

	private final ToDoRepository repository;
	private final ApplicationEventPublisher publisher;

	public ToDoController(ToDoRepository repository, ApplicationEventPublisher publisher) {
        this.repository = repository;
        this.publisher = publisher;
        for (var t: "read a book, go to the gym, learn HATEOAS".split(",")) {
			this.toDos.add(ToDos.toDo(t));
		}
	}

	@GetMapping
	String todos(Model model) {
		model.addAttribute("todos", this.toDos);
		return "todos";
	}

	@DeleteMapping(produces = MediaType.TEXT_HTML_VALUE, path = "/{toDoId}")
	@ResponseBody
	String delete(@PathVariable Integer toDoId) {
		this.toDos.stream()
				.filter(t -> t.id().equals(toDoId))
				.forEach(this.toDos::remove);
		return "";
	}

	@PostMapping
	View add(@RequestParam("new-todo") String newToDo, Model model) {
		this.toDos.add(ToDos.toDo(newToDo));
		model.addAttribute("todos", this.toDos);
		return FragmentsRendering
				.with("todos :: todos")
				.fragment("todos :: todos-form")
				.build();

	}

	@PostMapping("/reset")
	View reset(Model model) {
		this.publisher.publishEvent(new ToDosResetEvent());
		model.addAttribute("todos", this.repository.findAll());
		return FragmentsRendering
				.with("todos :: todos")
				.fragment("todos :: todos-list")
				.build();
	}
}

class ToDosResetEvent extends ApplicationEvent {
	public ToDosResetEvent() {
		super(Instant.now());
	}
}

record ToDo(Integer id, String title) {
}

class ToDos {
	private static final AtomicInteger id = new AtomicInteger(0);

	static ToDo toDo(String title) {
		return new ToDo(id.incrementAndGet(), title);
	}
}


interface ToDoRepository extends CrudRepository<ToDo, Integer> {
}

@Component
class Initializer {

	private final ToDoRepository repository;

    Initializer(ToDoRepository repository) {
        this.repository = repository;
    }

	@EventListener({ApplicationReadyEvent.class, ToDosResetEvent.class})
	void reset() {
		this.repository.deleteAll();
		Stream.of("Learn HTMX", "Learn Spring ViewComponent", "Learn Hotwire",
				"Make some coffee")
				.forEach(t -> this.repository.save(ToDos.toDo(t)));
	}
}