package com.cloudstream.source;

import com.fasterxml.jackson.annotation.JsonIgnoreProperties;
import lombok.Data;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.web.reactive.function.client.WebClient;
import reactor.core.publisher.Flux;

import java.util.function.Supplier;

@SpringBootApplication
public class SourceApplication {

	public static void main(String[] args) {
		SpringApplication.run(SourceApplication.class, args);
	}

}

@Configuration
class PositionReporter {
	private final WebClient client = WebClient.create("http://localhost:7634/aircraft");
	@Bean
	Supplier<Flux<Aircraft>> sendPositions() {

		return () -> client.get()
				.retrieve()
				.bodyToFlux(Aircraft.class)
	}
}

@Data
@JsonIgnoreProperties(ignoreUnknown = true)
class Aircraft {
	private String callsign, reg, flightno, type;
	private int altitude, heading, speed;
	private double lat, lon;
}